"""
build the page routes

"""

from loguru import logger
from nicegui import ui
from pages.examrender import exam_generator
from pages.examlist import examlist_generator
from pages.examlogin import examlogin_generator
from pages.examlogout import examlogout_generator
from pages.settings import settings_generator


def create() -> None:
    logger.info("Building page routes")
    ui.page("/examlist/")(examlist_generator)
    ui.page("/examlogin/")(examlist_generator)  # catch routes without an exam id
    ui.page("/examlogin/{examid}")(examlogin_generator)
    ui.page("/examlogout/")(examlogout_generator)
    ui.page("/exam/")(examlist_generator)  # catch routes without an exam id
    ui.page("/exam/{examid}")(exam_generator)  # must contain an id
    # catch anything after exam id
    ui.page("/exam/{examid}/{_:path}")(exam_generator)  # must contain an id
    ui.page("/settings/")(settings_generator)


if __name__ == "__main__":
    create()
