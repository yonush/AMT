"""
The settings page lets the learner set some settings before the exam can proceed.
The main setting is the address for the remote Assessment Delivery Server
The other two settings can be ignored

"""

from loguru import logger
from nicegui import ui

import config as cfg
import theme
from exam import Exam  # main assessment/exam driver


def settings_generator():
    logger.info(f"Navigating to /settings")
    _cfg = cfg.readConfig()

    def try_connect():  # local function to avoid passing username and password as arguments
        logger.info(f"Testing remote server connectivity")

        if Exam.testADS:
            ui.notify(
                "Successfully connected to the Assessment Delivery server",
                color="positive",
            )
        else:
            ui.notify(
                f"Unable to connect to the Assessment Delivery server", color="negative"
            )

    def updateSettings():
        # ensure session values are cleared
        Exam.sessionClear()
        Exam.URL = deliveryaddr.value
        _cfg.delivery_server = deliveryaddr.value
        _cfg.listen_port = listenport.value
        _cfg.host_addr = hostaddr.value
        cfg.updateConfig(_cfg)
        ui.notify("Settings successfully updated", color="positive")

    Exam.sessionLoad()
    with theme.frame("System settings"):
        ui.page_title("System settings")

        with ui.card().classes("fixed-center").style("border-left: 4px solid #6E93D6"):
            ui.label(f"System settings").style("font-size: 150%; font-weight: 1100")
            ui.restructured_text(
                """ 
                    Instructions:

                    - The test connection will check if the **Assessment Delivery server** is accessible. 
                    - The **Assessment Delivery server** address is the most important setting. It is not necessary to alter the other two settings.
                    - Updating the settings **will clear** any active session information.
                    - The **Assessment Delivery server** can be an IP address or domain name. The remote server listens on port 8088
                """
            ).style("font-size: 120%;")
            ui.separator()
            with ui.card_section():
                with ui.column():
                    try:  # catch the NoneType validation error when validating the value after a clear
                        deliveryaddr = ui.input(
                            "Assessment Delivery server address",
                            value=_cfg.delivery_server,
                        ).classes(
                            "w-full"
                        )  # .props("clearable")
                        listenport = ui.input(
                            "Listen port", value=str(_cfg.listen_port)
                        )  # .props("clearable")
                        hostaddr = ui.input(
                            "Local host address", value=_cfg.host_addr
                        )  # .props("clearable")
                    except:
                        pass

                with ui.row():
                    ui.separator()
                    ui.button(
                        "Test connection",
                        icon="settings_ethernet",
                        on_click=try_connect,
                    ).tooltip(
                        "Test for connectivity to the Assessment Delivery server"
                    ).classes(
                        replace="text-black"
                    )

                    ui.button(
                        "Update settings",
                        icon="settings",
                        on_click=lambda: updateSettings(),
                    ).tooltip("Update the system settings with the above").classes(
                        replace="text-black"
                    )
