"""
Query the Assessment delivery server to download a list of the current examinations
"""

from loguru import logger
from nicegui import ui

import theme
from exam import Exam  # main assessment/exam driver


# page generator
def examlist_generator():
    logger.info("Navigating to /examlist")

    examlist = Exam.getExamList()

    with theme.frame("Examination List"):
        ui.page_title("Examination List")
        # fix an anoying space above the label that hides the top message when the footer is showing
        ui.html("&nbsp",sanitize=False).style("font-size: 120%; font-weight: 800")
        with ui.column():
            ui.label("Select an exam using the ▶︎").style(
                "color: #6E93D6; font-size: 150%; font-weight: 800"
            )
            ui.label("使用▶︎选择考试").style(
                "color: #6E93D6; font-size: 150%; font-weight: 800"
            )
            ui.separator()
            # make sure exam lists contains some exams
            if len(examlist) > 0:
                for e in examlist:
                    exam_entry = f"{e["ExamID"]}: {e["Code"]} {e["Description"]}"
                    with ui.row():
                        ui.label(exam_entry).style(
                            "color: #A0A0A0; font-size: 150%; font-weight: 1100"
                        )
                        # take care of dots in the coursecode
                        # do a string replace to remove dot from examid
                        ui.link("▶︎", f"/examlogin/{e["ExamID"]}").classes(
                            "no-underline"
                        ).style("color: #6E93D6; font-size: 150%; font-weight: 1100")
            else:
                ui.label("Unable to retrieve the current exam list").style(
                    "color: #A0A0A0; font-size: 150%; font-weight: 1100"
                )
        ui.separator()
        ui.html("&nbsp",sanitize=False).style("font-size: 120%; font-weight: 800")
