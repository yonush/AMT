"""
Download an exam from the Assessment Delivery Server in JSON format and generate the exam page.
The exam ID in the form [course code][semester][year] is passed to the page as the exam key
e.g ITCS5.100S12025
    - course: ITCS5.100,Computer System Architecture
    - semester: semester 1
    - year: 2025

https://fonts.google.com/icons?icon.set=Material+Icons

"""

from loguru import logger
from nicegui import app, timer, ui

import menu  # required for the dynamic menu creation for the exam sections
import theme
from exam import Exam  # main assessment/exam driver

autosave = 0  # 5 minute counter for the autosave - see evt_timer()
examtmr: timer.Timer


def evtNull():
    pass


# general timer event for the exam autosave
def evtTimer() -> None:
    global autosave, examtmr
    """A 5sec timer event that updates. Updates the timer bar and autosaves the exam progress 
       every 5minutes. Also checks for expiring and triggers the end-of-examination state
    
    """

    # save the exam progress every 5 minutes
    autosave += 1
    if autosave >= 60:  # 60 * 5sec for 5min
        Exam.sessionLoad()
        Exam.saveExam()
        autosave = 0
    if Exam.isExpired:
        examtmr.deactivate()  # turn off the timer
        Exam.saveExam()
        theme.examtimer = False

        Exam.logout()
        ui.navigate.to(f"/#")
    # update the exam timer bar
    theme.ui_examtimer.refresh()


def evtSaveExam():
    if Exam.saveExam():
        ui.notify("Exam progress saved.", type="positive")
    else:
        ui.notify("Unable to save a copy of the exam progress.", color="negative")


def generateMenu(count: int) -> list:
    """Creates the side-bar menu for the sections quick links.
    Makes the menu available to the general menu render page menu.py

    Args:
        count (int): number of sections to add to the menu

    Returns:
        list: Updated menu
    """
    exam_menu = [
        ["← Home/主页", "/#"],
        ["Logout/登出", "/examlogout"],
        ["🔹Sections🔹", ""],
    ]

    localmenu = exam_menu.copy()
    for i in range(count):
        entry = [f"Section {i+1}", f"#section{i+1}"]
        localmenu.append(entry)
    return localmenu


def makeSection(ndx, section):
    """Generates a single section of the exam based on the question type.

    Args:
        ndx (int): The index of the section used for the internal page anchors
        section (dict): The a single section from the main exam.

    Returns:
       None
    """

    def buildInstructions(section: list) -> str:
        msg = "Instructions: "
        for v in section:
            msg += f"{v}\n"
        return msg

    def buildQuestion(question: dict) -> str:
        msg = ""
        Q = ""
        if isinstance(question["Question"], list):
            for v in question["Question"]:
                Q += f"{v}\n"
        else:
            Q = question["Question"].replace("~", "▪")  # replace ~ (tildes)
        msg += f"{Q}\n"

        return msg

    def buildAnswer(qtype: str, question: str, extra: list):
        if qtype == "TF":
            return (
                ui.radio({1: "True", 2: "False"}, value=1)
                .props(
                    'outlined use-chips filled dense label-color="teal" clearable standout="bg-teal2 text-white" inline'
                )
                .classes("m-1 w-full")
            )
        elif qtype == "MC":
            return (
                # ui.radio({1: "a", 2: "b", 3: "c", 4: "d", 5: "e"}, value=1)
                ui.radio([1, 2, 3, 4, 5], value=1)
                .props(
                    'outlined use-chips filled dense label-color="teal" clearable standout="bg-teal2 text-white" inline'
                )
                .classes("m-1 w-full")
            )

        elif qtype == "OWA":
            # check how many words are required - 5 = 1 word, 10 = 2 words, 15 = 3 words
            multi = question.count("~") > 5
            return (
                ui.select(
                    extra,
                    multiple=multi,
                    label="Answer - click here to add one or more words to your answer",
                )
                .props(
                    'outlined use-chips filled dense label-color="teal" clearable standout="bg-teal2 text-white"'
                )
                .classes("m-1 w-full")
            )
        elif qtype == "MAW":
            return (
                ui.select(
                    extra,
                    multiple=False,
                    label="Answer - click here to match the correct word/phrase to the question",
                )
                .props(
                    'outlined dense filled clearable label-color="teal" standout="bg-teal2 text-white"'
                )
                .classes("m-1 w-full")
            )
        elif qtype == "DI":
            # default to a standard input box
            return (
                ui.textarea(label="Answer - type in the correct answer")
                .props(
                    'outlined dense filled clearable label-color="teal" standout="bg-teal2 text-white"'
                )
                .classes("m-1 w-full")
            )
        else:
            # default to a standard input box
            return (
                ui.input("Answer - type in the answer for the above question")
                .props(
                    'outlined dense filled label-color="teal" standout="bg-teal2 text-white" clearable'
                )
                .classes("m-1 w-full")
            )

    """
        ...
            {
                "Title": "",
                "Qtype": "",
                "Instruction": "", 
                "OutofMark": 0,
                "Extra":"",
                "Questions": [ ],            
            }
        ...
    """
    with ui.card().tight().style("border-left: 4px solid #6E93D6").classes(
        "w-[1000px]"
    ):
        ui.html(f'<div id="section{ndx+1}">', sanitize=False)
        with ui.row().classes("w-full"):
            # Section Header
            ui.label(section["Title"]).style(
                "color: #6E93D6; font-size: 130%; font-weight: 800"
            ).classes("m-5")

            ui.space()
            ui.label(Exam.questiontype[section["Qtype"]]).style(
                "color: #6E93D6; font-size: 130%; font-weight: 800"
            ).classes("m-5")

            ui.space()
            ui.label(f"Marks: {section["OutofMark"]}").style(
                "color: #6E93D6; font-size: 130%; font-weight: 800"
            ).classes("m-5")

        if isinstance(section["Instruction"], list):
            ui.markdown(buildInstructions(section["Instruction"])).classes(
                "m-1 w-full"
            ).style("font-size: 110%; font-weight: 600")
        elif bool(section["Instruction"]):
            ui.label(f"Instructions: {section["Instruction"]}").classes(
                "m-1 w-full"
            ).style("font-size: 110%; font-weight: 600")
        else:
            ui.label(f"Instructions: None").classes("m-1 w-full").style(
                "font-size: 110%; font-weight: 600"
            )
        ui.html("</div>", sanitize=False)
        ui.separator()

        """
            ...
            {
                "Qtype": "",
                "Question": "",
                "Solution": "",
                "Answer": "",
                "Mark": 0,
                "Outof": 0
            }
            ...
        """
        # exam question body
        with ui.card_section():
            question = 1
            with ui.row().classes("w-full"):
                for Q in section["Questions"]:
                    with ui.column().classes("w-full"):
                        ui.separator().props('color="teal"')
                        with ui.row().classes("w-full my-[2]"):
                            ui.label(f"Question: {question}").style(
                                "color: #008080;font-size: 110%; font-weight: 700"
                            ).classes("my-1 w-50 full text-right")
                            ui.space()
                            ui.label(f"{Q["Outof"]} mark/s").classes(
                                "my-1 w-50 text-right"
                            ).style("color: #008080;font-size: 110%; font-weight: 700")
                        ui.markdown(buildQuestion(Q)).classes("m-1 w-full")
                        with ui.row().classes("w-full"):
                            # grab current answer even if it might be blank
                            ans = Q["Answer"]
                            Exam.answers.append(
                                buildAnswer(
                                    section["Qtype"],
                                    Q["Question"],
                                    section["Extra"],
                                )
                            )
                            # transfer over the answer after creating the control
                            Exam.answers[-1].value = ans
                        ui.html("&nbsp;", sanitize=False)
                        question += 1


def exam_generator(examid: str = ""):
    global examtmr

    # section pre-processor
    def preprocess():
        # iterate over each section
        for sec in Exam.data["Exam"]["Sections"]:
            extra = []  # start with empty list for each section
            # iterate over each question in the target section  - OWA or MAW
            if sec["Qtype"] == "OWA" or sec["Qtype"] == "MAW":
                for Q in sec["Questions"]:
                    # copy over the list of the value is a list
                    if isinstance(Q["Solution"], list):
                        extra.extend(Q["Solution"])
                    else:
                        extra.append(Q["Solution"])
                extra.sort()  # sort the list to remove ordering
                sec["Extra"] = extra.copy()

    Exam.sessionLoad()
    logger.info(f"Navigating to /exam/{Exam.assessmentid}")
    # must be authenticated before attempting the exam

    if not Exam.isAuthenticated or Exam.starttime == 0:
        ui.navigate.to(f"/examlist/")

    # retrieve the current exam
    if Exam.testADS():
        Exam.getExam()
        if bool(Exam.data):
            # we assume the exam time is an actual number
            Exam.duration = int(Exam.data["Metadata"]["ExamTime"])
            preprocess()

            # start the timer and turn on the timer bar

            # if by chance the timer does not exist
            if "examtmr" not in globals():
                logger.debug(f"- creating the exam timer")
                examtmr = app.timer(
                    5, evtTimer, immediate=False
                )  # 30 sec interval timer
            examtmr.activate()
            theme.examtimer = True
        else:
            ui.notify("Assessment delivery not authorised.", color="negative")
            ui.navigate.to(f"/#")
    else:
        if "examtmr" in globals():
            examtmr.deactivate()
        theme.examtimer = False
        Exam.duration = 0
        Exam.data = {}
        ui.notify("Assessment Delivery Server unavailable.", color="negative")

    # build the menu before showing the UI
    examtitle = ""
    if bool(Exam.data):
        # generate the inpage anchors menu based on the sections
        menu.external_menu = generateMenu(len(Exam.data["Exam"]["Sections"]))
        examtitle = f"{Exam.data["Metadata"]["CourseCode"]} {Exam.data["Metadata"]["Course"]} - Duration {Exam.data["Metadata"]["ExamTime"]} minutes"

    """
    {
        "Metadata":{
        "ExamID": "2025S1ITCS5.100",
        "ExamTime": 90,
        "Program": "BCS",
        "Level": 5,
        "Weight": 20,
        "CourseCode": "ITCS5.100",
        "Course": "Computer System Architecture",
        "OutofMark": 80,
        "StudentID": "",
        "password": "",
        "Mark":0,
        "TimeStart":0,
        "TimeEnd":0
        },
        "Exam": {}
    } 

"""

    # create the examination page
    with theme.frame("Exam Generator"):
        ui.page_title("Examination")
        # spacer used to shift content below the menu bar
        # ui.html("&nbsp;").style("font-size: 130%;")
        ui.html("&nbsp;", sanitize=False).classes("py-2")
        ui.label(
            f"Examination for {Exam.assessmentid}. Student ID: {Exam.studentid}"
        ).style("color: #6E93D6; font-size: 150%; font-weight: 800")
        ui.label(examtitle).style("color: #6E93D6; font-size: 150%; font-weight: 800")

        # make sure the exam contains suitable data
        if bool(Exam.data):
            for k, section in enumerate(Exam.data["Exam"]["Sections"]):
                makeSection(k, section)
            # ui.markdown(exa)
            ui.html("&nbsp;", sanitize=False).classes("py-4")
    with ui.page_sticky(position="bottom-right", x_offset=20, y_offset=20):
        ui.button(on_click=evtSaveExam, icon="assignment_turned_in").props(
            "fab"
        ).tooltip("Save your exam progress.")
