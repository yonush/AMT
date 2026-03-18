"""
build the left side bar menus based on the current route.

"""

from loguru import logger
from nicegui import ui

from exam import Exam  # main assessment/exam driver

# if the menu is created outside of this page in the case of pages/exam.py
external_menu: list[list] = []


def main_menu() -> None:
    Exam.sessionLoad()
    stub = ui.context.client.sub_pages_router.current_path
    logger.debug(f"Generating menu for route {stub}")
    # menu hack to display context menu based on a route
    # url = str(ui.context.client.request.url)
    # pg = url.replace(str(ui.context.client.request.base_url),"")

    # prepare the menus based off the currently selected route stub
    if stub == "/settings/":
        links = [
            ["← Home", "/#"],
        ]
    else:
        links = [
            ["Mark\nexams ➡", "/#"],
            ["Exam\nbuilder", "/#"],
            ["Reports", "/#"],
            ["_______", ""],
            ["Logout", "/logout"],
            ["Shutdown", "/shutdown"],
            ["Settings", "/settings"],
        ]

    # generate the menu based on the route type - URL or text
    for link in links:
        # check if its a label or link
        if len(link[1]) > 0:
            ui.link(link[0], link[1]).classes(replace="text-black").style(
                "font-size: 80%"
            )
        else:
            ui.label(link[0]).classes(replace="text-black").style("font-size: 80%")
