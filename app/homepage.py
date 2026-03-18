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
        if Exam.isAuthenticated and not Exam.isExpired:
            with ui.row().classes("w-full").props("height=85"):
                ui.restructured_text(
                    """
                    To successfully log out of the current assessment,
                    you **must** click 'Continue exam' then 'Logout'.
                    This will ensure your assessment is properly saved.                                     
                                     """
                ).style("color: #8B0000;font-size: 130%; font-weight: 700")

        ui.restructured_text(
            """ 
                Instructions:

                - This is a closed book exam. 
                - Answer all the questions in English, in the areas provided.
                - No unauthorised resources or communication with others are allowed. 
                - You MUST answer ALL questions.
                - Answer the questions in the areas provided.
                - Use of the Internet is NOT permitted. 
                - Activity is monitored during the exam.

                指示：

                - 这是一个闭卷考试
                - 在提供的区域用英语回答所有问题
                - 不允许使用未经授权的资源或与他人通信
                - 您必须回答所有问题
                - 不允许使用互联网
                - 考试期间监控活动
                """
        ).style("font-size: 120%; font-weight: 700")

        ui.html("&nbsp;&nbsp;&nbsp;&nbsp;",sanitize=False)  # lazy spacer :)
        ui.separator()
        with ui.card_section():
            with ui.row():

                ui.button(
                    "Continue with exam/继续考试",
                    icon="assessment",
                    # on_click=lambda: try_nav(),
                    on_click=lambda: ui.navigate.to(f"/trylogin"),
                ).tooltip("Start with the examination").classes(replace="text-black")

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
