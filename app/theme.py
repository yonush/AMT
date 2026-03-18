"""
Theme used for all of the page content

    https://unicode.org/Public/emoji/16.0/emoji-test.txt
    https://quasar.dev/docs
    https://quasar.dev/style/color-palette#brand-colors
    https://tailwindcss.com/docs/installation/using-vite
    https://nicegui.io/documentation
    https://fonts.google.com/icons?icon.set=Material+Icons
    https://www.plus2net.com/python/tkinter-colors.php
"""

from contextlib import contextmanager
from time import localtime

from nicegui import html, ui

import menu
from exam import Exam  # main assessment/exam driver

left_drawer: ui.left_drawer


@ui.refreshable
def ui_datetime() -> None:
    """Show the current time - refreshed every second from event in main.py"""
    tm = localtime()
    ui.label(
        f"{tm.tm_mday}/{tm.tm_mon}/{tm.tm_year} {tm.tm_hour}:{tm.tm_min:0>2}:{tm.tm_sec:0>2}"
    ).style("font-size: 130%; border-left: 4px solid #6E93D6;")


# provide a visible exam timer based on when the learner has logged into the exam
@ui.refreshable
def ui_examtimer() -> None:
    pass


def logout():
    ui.navigate.to("/logout")


# here we use our custom page decorator directly and just put the content creation into a separate function
@contextmanager
def frame(navtitle: str):
    Exam.sessionLoad()
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.query("html").style("overflow-y: scroll;")
    ui.colors(
        primary="#6E93D6", secondary="#53B689", accent="#111B1E", positive="#53B689"
    )
    with ui.column().classes(
        "absolute-center items-center h-screen p-9 w-full"
    ):  # removed no-wrap
        yield
    with ui.header().classes(replace="row items-center") as header:
        ui.image("app/eit_logo.png").classes("w-[130px] justify-end").style(
            "border-left: 4px solid #6E93D6; border-bottom: 2px solid #6E93D6;"
        )

        # ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props("flat color=white")
        ui_datetime()  # show the time
        ui.label("Assessment Marking Tool").style("font-size: 200%").classes(
            "absolute-center"
        )
        ui.button(on_click=logout, icon="logout").props("outline round")

    with ui.footer(value=True).classes("bg-blue-100").style(
        "border-left: 4px solid #6E93D6"
    ) as footer:
        with ui.row().classes("w-full").props("height=85"):
            ui.label("Copyright © 2026 EIT ").style("color: #27408B;")
            ui.space()
            if Exam.isAuthenticated:
                ui.label(f"LOGGED IN TO {Exam.assessmentid} AS {Exam.studentid}").style(
                    "color: #008080;font-size: 130%; font-weight: 700"
                )
            else:
                ui.label("LOGGED OUT").style(
                    "color: #8B0000;font-size: 130%; font-weight: 700"
                )
            ui.space()
            ui.label("Created by John Jamieson").style("color: #27408B;")
    with ui.left_drawer().classes("bg-blue-100").props("width=130").style(
        "border-left: 4px solid #6E93D6"
    ) as left_drawer:
        html.strong("🔹Menu🔹")
        with ui.column():
            menu.main_menu()
            # dark = ui.dark_mode()
            # ui.switch("Dark/黑暗").bind_value(dark)

    # with ui.page_sticky(position="bottom-right", x_offset=20, y_offset=20):
    #   ui.button(on_click=footer.toggle, icon="assignment_turned_in").props("fab")
