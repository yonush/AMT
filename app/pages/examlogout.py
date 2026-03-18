"""
The logout requires no arguments to logout - the session information used for this page
The exam is saved in a plaintext JSON format and sent to the Assessment Delivery Server
The exam session information is then cleared
"""

from loguru import logger
from nicegui import ui

import theme
from exam import Exam  # main assessment/exam driver


def try_logout():
    if Exam.isAuthenticated:
        theme.examtimer = False
        Exam.logout()
        ui.notify("You have successfully logged out", color="positive")
        ui.navigate.to(f"/#")
    else:
        ui.notify("You have already logged out", color="negative")


# Removes the session information for the current learner hence logging them out of the exam.
def examlogout_generator():
    logger.info(f"Navigating to /examlogout, logging out from {Exam.assessmentid}")

    with theme.frame("Exam save and close"):
        ui.page_title("Exam save and close")
        with ui.card().classes("fixed-center").style("border-left: 4px solid #6E93D6"):
            ui.label(f"Examination: {Exam.assessmentid}").style(
                "color: #6E93D6; font-size: 150%; font-weight: 800"
            )
            ui.label(f"You will be  logged out of the above examination.").style(
                "color: #6E93D6; font-size: 150%; font-weight: 800"
            )
            ui.label("您已退出上述考试。").style(
                "color: #6E93D6; font-size: 150%; font-weight: 800"
            )
            ui.restructured_text(
                """ 
                    **NOTE**

                    - Logging out of the exam will clear all of the examination session information. 
                    - This finalises your examination and records the exam time.
                    - The exam will be saved before logging out.
                    - Any cached examination information will be erased after logging out.        
                    - Saving the exam prevents any futher attempts of the examination
                    """
            ).style("font-size: 120%; font-weight: 700")

            ui.html("&nbsp;&nbsp;&nbsp;&nbsp;",sanitize=False)  # lazy spacer :)
            with ui.card_section():
                with ui.row():
                    ui.button(
                        "Logout",
                        icon="logout",
                        on_click=try_logout,
                    ).tooltip(
                        "Logout of the the examination"
                    ).classes(replace="text-black")

                    ui.button(
                        "Home/主页", on_click=lambda: ui.navigate.to(f"/")
                    ).tooltip("Return home").classes(replace="text-black")
