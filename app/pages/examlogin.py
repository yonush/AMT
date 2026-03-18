"""
The login requires three arguments to proceed with the examination - examination ID, learner ID and the exam password
This authenticates a learner and authorises them for the exam.
The learner student ID is used to authenticate the attendence for and exam
The password is used to authorise the access to the examination based on the password.

"""

import theme
from exam import Exam  # main assessment/exam driver
from loguru import logger
from nicegui import ui


# Exam login page generator
def examlogin_generator(examid: str = ""):
    logger.info(f"Navigating to /examlogin, logging into {examid}")

    # reference: nicegui/examples/authentication/main.py
    def try_login():  # local function to avoid passing username and password as arguments

        if Exam.isAuthenticated:
            ui.navigate.to(f"/exam/{Exam.assessmentid}")

        if Exam.login(examid, studentid.value, password.value):
            ui.notify("Successfully logged in", color="positive")

            ui.navigate.to(f"/exam/{examid}")
        else:
            ui.notify(
                "Unable to authorise the exam with this username and password",
                color="negative",
            )

    with theme.frame("Examination Login"):
        ui.page_title("Examination Login")

        with ui.card().classes("fixed-center").style("border-left: 4px solid #6E93D6"):
            ui.label(f"Examination Login for exam {examid}").style(
                "font-size: 150%; font-weight: 1100"
            )
            ui.restructured_text(
                """ 
                    Instructions:

                    - The exam code should match the one provided by the invigilator/s                        
                    - Enter in your student ID as per your student card.
                    - Use the exam password as provided by the invigilator/s.
                    - Your exam progress is saved every 5 minutes.
                    - At the end of the exam time the exam will save and automatically end.
                    
                    指示：

                    - 考试代码应与监考人员提供的考试代码一致。
                    - 根据您的学生证输入您的学生证号。
                    - 使用监考人员提供的考试密码。
                    """
            ).style("font-size: 120%; font-weight: 700")

            ui.separator()
            with ui.card_section():
                ui.label(f"Exam ID: {examid}").style(
                    "color: #A0A0A0; font-size: 150%; font-weight: 1100"
                )
                with ui.row():
                    try:  # catch the NoneType validation error when validating the value after a clear
                        studentid = ui.input(
                            "Student ID/学生证",
                            validation=lambda value: (
                                "ID too short" if len(value) < 8 else None
                            ),
                        )  # .props("clearable")
                        password = ui.input(
                            "Exam password/考试密码",
                            validation=lambda value: (
                                "Password too short" if len(value) < 8 else None
                            ),
                        )  # .props("clearable")
                    except:
                        pass

                with ui.row():
                    ui.button(
                        "Continue with exam/继续考试",
                        icon="login",
                        on_click=try_login,
                    ).tooltip("Start the examination").classes(replace="text-black")

                    ui.button(
                        "Back to the exam List/返回考试列表",
                        icon="assessment",
                        on_click=lambda: ui.navigate.to(f"/examlist/"),
                    ).tooltip("Return back to the exam selection list").classes(
                        replace="text-black"
                    )
