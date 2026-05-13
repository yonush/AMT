import requests
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import app, ui

from exam import Exam  # main assessment/exam driver


@app.get("/trylogin")
async def redirect_login():
    if Exam.isAuthenticated:
        return RedirectResponse(f"/exam/{Exam.assessmentid}")
    else:
        return RedirectResponse(f"/examlist")
        # ui.navigate.to(f"/examlist")


def content() -> None:
    # reference: nicegui/examples/authentication/main.py
    def try_connect():  # local function to avoid passing username and password as arguments
        logger.info(f"Testing remote server connectivity")

        if Exam.testADS():
            ui.notify(
                "Successfully connected to the Assessment Delivery server",
                color="positive",
            )
        else:
            ui.notify(
                f"Unable to connect to the Assessment Delivery server", color="negative"
            )

    def try_nav():
        if Exam.isAuthenticated:
            logger.info(f"Navigating to /examlogin, logging into {Exam.assessmentid}")
            RedirectResponse(f"/exam/{Exam.assessmentid}")
            # ui.navigate.to(f"/exam/{Exam.assessmentid}")
        else:
            ui.navigate.to(f"/examlist")

    with ui.card().classes("fixed-center").style("border-left: 4px solid #6E93D6"):

        ui.restructured_text(""" 
                Quick help:

                - Use the "Mark Exams" menu to manually and automark exams - bulk and individual.
                - Use the "Exam Builder" menu to create and manage individual exam offerings. 
                - Use the Reports menu to generate class lists, grades and active exam offerings. 
                - Use the Admin menu for settings, password changes, etc.

                
                """).style("font-size: 120%; font-weight: 700")

        ui.html("&nbsp;&nbsp;&nbsp;&nbsp;", sanitize=False)  # lazy spacer :)
        ui.separator()
        with ui.card_section():
            with ui.row():

                ui.button(
                    "Shutdown/关闭",
                    icon="exit_to_app",
                    on_click=lambda: ui.navigate.to(f"/shutdown"),
                ).tooltip("Shutdown the system").classes(replace="text-black")

                ui.button(
                    "Test Assessment Delivery server connection",
                    icon="settings_ethernet",
                    on_click=try_connect,
                ).tooltip(
                    "Test for connectivity to the Assessment Delivery server"
                ).classes(
                    replace="text-black"
                )
