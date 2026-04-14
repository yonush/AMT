"""
build the left side bar menus based on the current route.

"""

from exam import Exam  # main assessment/exam driver
from loguru import logger
from nicegui import ui

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
    elif "/builder" in stub:
        links = [
            ["New exam", "/newexam"],
            ["Manage Exam", "/manexam"],
            ["Archive Exam", "/archexam"],
            ["_______", ""],
            ["← Home", "/#"],
        ]
    elif "/marker" in stub:
        links = [
            ["List Unmarked", "/examunmarked"],
            ["Premark Exams", "/exampremark"],
            ["Manual Mark", "/exammanual"],
            ["Backup Exams", "/exambackup"],
            ["_______", ""],
            ["← Home", "/#"],
        ]
    elif "/reports" in stub:
        links = [
            ["Current Exams", "/rptexam"],
            ["Exams by Course", "/rptcourse"],
            ["Grades by Learner", "/rptgrades"],
            ["_______", ""],
            ["← Home", "/#"],
        ]

    else:
        links = [
            ["Mark exams ➡", "/marker"],
            ["Exam builder ➡", "/builder"],
            ["Reports ➡", "/reports"],
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
