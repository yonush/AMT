"""
https://unicode.org/Public/emoji/16.0/emoji-test.txt
https://quasar.dev/docs
https://tailwindcss.com/docs/installation/using-vite
https://nicegui.io/documentation

pip install psutil
pip install keyboard
pip install loguru
pip install nicegui
"""

import sys
import time
from typing import Optional

import keyboard  # used to close the browser page
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import Client, app, html, ui
from nicegui.events import ValueChangeEventArguments
from nicegui.page import page
from starlette.middleware.base import BaseHTTPMiddleware

import config as cfg
import exam  # main assessment/exam driver
import homepage
import page_builder
import theme

isFullscreen = False
exam.Exam = exam.Assessment()
Exam = exam.Exam

passwords = {"user1": "pass1", "user2": "pass2"}
unrestricted_page_routes = {"/login", "/logout"}


@app.exception_handler(404)
async def exception_handler_404(request: Request, exception: Exception) -> Response:
    logger.debug(f"404 page not found error on {request.url}")
    with Client(page(""), request=request) as client:
        with theme.frame("error"):
            with ui.card().classes("error-card fixed-center"):
                ui.label("Sorry, this page does not exist").classes("heading").style(
                    "color: #6E93D6; font-size: 200%; font-weight: 1200"
                )

    return client.build_response(request, 404)


@app.exception_handler(500)
async def exception_handler_500(request: Request, exception: Exception) -> Response:
    logger.debug(f"500 error on {request.url}")
    with Client(page(""), request=request) as client:
        with theme.frame("error"):
            with ui.card().classes("error-card fixed-center"):
                ui.label("500 Application Error").classes("heading").style(
                    "color: #6E93D6; font-size: 200%; font-weight: 1200"
                )
    return client.build_response(request, 500)


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.
    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get("authenticated", False):
            if (
                not request.url.path.startswith("/_nicegui")
                and request.url.path not in unrestricted_page_routes
            ):
                return RedirectResponse(f"/login?redirect_to={request.url.path}")
        return await call_next(request)


# navigate to the home/main page
@ui.page("/")
def index_page() -> None:
    logger.info("Navigating to main /")
    # https://nicegui.io/documentation/storage
    """
        session storage to include logged in status
        other session values to be confirmed

    """
    Exam.sessionLoad()

    with theme.frame("Main"):
        homepage.content()


@ui.page("/logout")
def logout_page() -> None:
    app.storage.user.clear()
    ui.navigate.to("/login")


@ui.page("/login")
def login(redirect_to: str = "/") -> Optional[RedirectResponse]:

    def try_login() -> (
        None
    ):  # local function to avoid passing username and password as arguments
        if passwords.get(username.value) == password.value:
            app.storage.user.update({"username": username.value, "authenticated": True})
            ui.navigate.to(redirect_to)  # go back to where the user wanted to go
        else:
            ui.notify("Wrong username or password", color="negative")

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")

    with ui.card().classes("absolute-center").style("border-left: 4px solid #6E93D6"):
        ui.image("app/eit_logo.png")
        ui.label("Assessment Management Tool").style("color: #27408B;font-size:150%")
        with ui.card_section():
            username = ui.input("Username").on("keydown.enter", try_login)
            password = ui.input(
                "Password", password=True, password_toggle_button=True
            ).on("keydown.enter", try_login)

            with ui.row().style("margin:10px"):
                ui.button(
                    "Login",
                    icon="login",
                    on_click=try_login,
                ).tooltip(
                    "Login to the system"
                ).classes(replace="text-black")
                ui.button(
                    "Shutdown the service",
                    icon="exit_to_app",
                    on_click=evtShutdown,
                ).tooltip("Shutdown the AMT system").classes(replace="text-black")

            ui.label("Copyright © 2026 EIT ").style("color: #27408B;")
    return None


def evtShow(event: ValueChangeEventArguments):
    logger.info("Triggering event: Show")
    name = type(event.sender).__name__
    ui.notify(f"{name}: {event.value}")


# NOTE: check if there is a pending exam before shutting down
def evtOn_Shutdown():
    """Shutdown the entire HMI including shutting down the com port
    before exiting the application
    """
    logger.warning("Shutting down the AMT app")
    app.timer(1, evtNull, active=False)

    keyboard.press_and_release("ctrl+F4")  # close browser tab
    time.sleep(1)  # delay 1 seconds


def evtOn_Startup() -> None:
    pass


def evtNull():
    pass


@ui.page("/shutdown")
def evtShutdown() -> None:
    app.shutdown()


# general UI refresh timer event
def evtUI_update() -> None:
    """A timer event that updates the UI at a regular interval - 1sec"""
    theme.ui_datetime.refresh()
    # theme.ui_examtimer.refresh()


# load all of the pages used by the application
page_builder.create()

if __name__ in {"__main__", "__mp_main__"}:
    logger.info("Starting the Assessment Management Tool")

    _cfg = cfg.readConfig()
    Exam.URL = _cfg.delivery_server
    # check if a port address has been passed to the app - defaults to 8080
    if len(sys.argv) > 1:
        try:
            _cfg.listen_port = int(sys.argv[1])
        except:
            _cfg.listen_port = 8080
    logger.info(f"Using {_cfg.delivery_server}:8088 for the ADS address.")
    app.add_middleware(AuthMiddleware)
    app.on_shutdown(evtOn_Shutdown)
    app.on_startup(evtOn_Startup)
    app.timer(1, evtUI_update, immediate=False)
    ui.run(
        storage_secret=_cfg.cookie_secret,
        host=_cfg.host_addr,
        port=_cfg.listen_port,
        reload=False,
        show=True,  # change to False to work with R3dfox
        title="Assessment Management Tool",
        reconnect_timeout=2,
    )
