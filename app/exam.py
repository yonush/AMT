import json
import pathlib  # https://docs.python.org/3/library/pathlib.html
import time
from typing import Any

import requests
from loguru import logger
from nicegui import app

import zipstream


# based off the Singleton metaclass
class Assessment:
    # used to prevent another copy of the examination
    _isinitialized: bool = False
    _instance: "Assessment | None" = None
    questiontype = {
        "MC": "Multi-Choice/Acronyms",
        "OWA": "Fill in the blanks",
        "MAW": "Match a Word or Phrase",
        "TF": "True/False",
        "SA": "Short Answers",
        "DI": "Discussion/Long Answer",
        "DND": "Drag n Drop",
        "MTP": "Match the Picture",
    }

    # """
    def __new__(cls, *args: Any, **kwargs: Any) -> "Assessment":
        if not isinstance(cls._instance, cls):
            # if cls._instance is None:
            # cls._instance = super(Singleton,cls).__new__(cls, *args, **kwargs)
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    # """

    def __init__(self) -> None:

        if not self._isinitialized:
            self._isinitialized = True

            # three main attributes required to attend an assessment
            self._assessmentid = ""
            self._studentid = ""
            self._password = ""

            # assessement controls
            self._authenticated = False
            self._starttime: int = 0
            self._duration: int = 0
            self._isexpired = False

            self._assessmentdata: dict[Any, Any] = {}
            self.answers: list = []  # exam answers as UI input objects

            self._URL: str = "localhost"

    @property
    def isExpired(self) -> bool:
        """Attempt to set the session value for authenticate. If it fails the volatile version is still active"""
        # check duration
        if self.duration > 0 and self.starttime > 0:
            currentTime = int(time.time())  # only use the seconds
            elapsed = currentTime - self.starttime
            if elapsed > self.duration:
                self._isexpired = True  # exam has expired
        return self._isexpired

    @property
    def elapsedpct(self):
        """Return the elapsed time as a % of the assessment duration"""
        if self._duration > 0 and self._starttime > 0:
            currentTime = int(time.time())
            elapsed = currentTime - self.starttime
            pct = (self.duration - elapsed) / self.duration
            if elapsed > self.duration:
                pct = 0
        else:
            pct = 0
        return pct

    @property
    def duration(self) -> int:
        # self.sessionLoad()
        return self._duration

    @duration.setter
    def duration(self, value: int):
        """Attempt to set the session value for duration. If it fails the volatile version is still active"""
        if not value:
            raise ValueError
        if not isinstance(value, int):
            raise ValueError
        if value < 0:
            raise ValueError

        try:
            self._duration = value * 60  # this is in seconds
            app.storage.user["duration"] = self._duration
        except ValueError:
            logger.warning("Unable to set session value for 'duration'")

    @property
    def isAuthenticated(self) -> bool:
        # self.sessionLoad()
        return self._authenticated

    @isAuthenticated.setter
    def isAuthenticated(self, value: bool):
        """Attempt to set the session value for authenticate. If it fails the volatile version is still active"""
        try:
            self._authenticated = value
            app.storage.user["authenticated"] = value
        except ValueError:
            logger.warning("Unable to set session value for 'authenticated'")

    @property
    def assessmentid(self) -> str:
        # self.sessionLoad()
        return self._assessmentid

    @assessmentid.setter
    def assessmentid(self, value: str):
        if not value:
            raise ValueError
        if not isinstance(value, str):
            raise ValueError
        try:
            self._assessmentid = value
            app.storage.user["assessmentid"] = value
        except ValueError:
            logger.warning("Unable to set session value for 'authenticated'")
        self._assessmentid = value

    @property
    def studentid(self) -> str:
        # self.sessionLoad()
        return self._studentid

    @studentid.setter
    def studentid(self, value: str):
        if not value:
            raise ValueError
        if not isinstance(value, str):
            raise ValueError
        try:
            self._studentid = value
            app.storage.user["studentid"] = value
        except ValueError:
            logger.warning("Unable to set session value for 'studentid'")
        self._studentid = value

    @property
    def password(self) -> str:
        # self.sessionLoad()
        return self._password

    @password.setter
    def password(self, value: str):
        if not value:
            raise ValueError
        if not isinstance(value, str):
            raise ValueError
        try:
            self._password = value
            app.storage.user["password"] = value
        except:
            logger.warning("Unable to set session value for 'studentid'")
        self._password = value

    @property
    def starttime(self) -> int:
        # self.sessionLoad()
        return self._starttime

    @starttime.setter
    def starttime(self, value: int):
        if not value:
            raise ValueError
        if not isinstance(value, int):
            raise ValueError
        if value < 0:
            raise ValueError
        try:
            self._starttime = value
            app.storage.user["starttime"] = value
        except ValueError:
            logger.warning("Unable to set session value for 'starttime'")
        self._starttime = value

    @property
    def URL(self) -> str:
        return self._URL

    @URL.setter
    def URL(self, value: str):
        if not value:
            raise ValueError
        if not isinstance(value, str):
            raise ValueError
        self._URL = value

    @property
    def data(self) -> dict[Any, Any]:
        return self._assessmentdata

    @data.setter
    def data(self, value: dict[Any, Any]):
        # if not value: raise ValueError
        # if not isinstance(value, dict): raise ValueError
        self._assessmentdata = value

    """
    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, value: str) -> "Grades":
        if not value:
            raise ValueError
        self._code = value
        return self
    """

    # reference: nicegui/examples/authentication/main.py
    # reference: nicegui/examples/authentication/main.py
    def testADS(self) -> bool:
        """Test if the Assessment delivery server is online

        Args:
            None

        Returns:
            bool: True if online or False if offline
        """
        URL = f"http://{self.URL}:8088/hello"
        query_parameters = {
            "downloadformat": "html",
        }
        try:
            requests.get(URL, params=query_parameters, timeout=1.5)
            logger.info(
                f"Successfully connected to the Assessment Delivery server on {self.URL}:8088"
            )
            return True
        except:
            logger.error(
                f"Unable to connect to the Assessment Delivery server on {self.URL}:8088"
            )
            return False

    def getExamList(self) -> list:
        """This function communicates with the delivery server to retrieve
        the current exam list as JSON.

        Args:
            None

        Returns:
            list: list of the current exams

        """

        URL = f"http://{Exam.URL}:8088/examlist"
        query_parameters = {"downloadformat": "json"}

        logger.info("Retrieving exam list")
        exams = []
        try:
            # """
            # retrieve the current examlist from the ADS
            response = requests.get(URL, params=query_parameters)
            data = json.loads(response.text)
            for row in data:
                exams.append(row)
            # """
            """
            cwd = os.getcwd()  # relative to the zat.exe
            with open(f"{cwd}\\app\\courses.json", "r") as f:
                # reader = csv.reader(f)
                reader = json.load(f)
                for row in reader:
                    exams.append(row)
            #"""
        except:
            logger.error(f"courses list data not found")
        return exams

    # check if the learner can login into the exam
    def login(self, assessmentid: str, studentid: str, password: str) -> bool:
        """This function communicates with the delivery server to check if the learner
        is to write the indicated exam.

        Args:
            studentid (string): Learner student ID
            examid (string): exam id for the exam to check against the Learner
            password( string): exam password, not student
        Returns:
            string: the password for the authorised exam for the learner
        """
        if not assessmentid or not studentid or not password:
            return False

        logger.info(f"Checking authorisation for {studentid}, exam {assessmentid}")
        msg = {}
        URL = f"http://{self.URL}:8088/auth/{assessmentid}/{studentid}"
        query_parameters = {"downloadformat": "json"}

        try:
            response = requests.get(URL, params=query_parameters)
            # data = json.loads(response.text)
            msg = response.json()
        except:
            logger.error(f"Unable to perform the authentication")

        if (
            msg["Status"] == "OK"
            and studentid == msg["studentid"]
            and assessmentid == msg["examid"]
            and password == msg["password"]
        ):
            # set local and sessions
            self.assessmentid = assessmentid
            self.studentid = studentid
            self.password = password
            self.isAuthenticated = True
            self.starttime = int(time.time())  # start the exam time
            logger.info(
                f"Login to {self.assessmentid} for {self.studentid} with {self.password} successful"
            )
            return True
        else:
            self.isAuthenticated = False
            logger.warning(
                f"Unable to login {studentid} for assessment {self.assessmentid} - {msg["Message"]}"
            )
            return False

    def saveExam(self, final: bool = False):
        """Saves the exam back to the ADS. A copy is cached on the local machine in the event communications
        to the server is problematic. Cached exam is removed once the learner has logged out.

        Args:
            None

        Returns:
        None
        """

        # exam has already expired, cannot save it after the time
        if self.isExpired:
            self.purgeExam()
            return False

        exam = {
            "token": self.password,
            "exam": "",
        }
        extension = "zip"  # extension for the file type to upload

        URL = f"http://{self.URL}:8088/examupload/{self.studentid}/{self.assessmentid}/{self.password}"

        # transfer the answers to the exam document - assume the question ordering has not changed
        ndx = 0
        for S in self.data["Exam"]["Sections"]:
            for Q in S["Questions"]:
                # WARNING the answers have a Nicegui input controls dependency to retrieve the current value
                # need to refactor to make the answer access less reliant on Nicegui
                Q["Answer"] = self.answers[ndx].value
                ndx += 1

        # update any outstanding metadata
        # studentID could have been set before an exam is loaded, so we make sure it is in the JSON
        self.data["Metadata"]["StudentID"] = self.studentid
        # the last save should be the final time of the exam
        ## use obj = time.gmtime(int([timestamp])) to decode
        self.data["Metadata"]["TimeStart"] = self.starttime
        self.data["Metadata"]["TimeEnd"] = int(time.time())
        # response: requests.Response

        # convert to JSON then send off to the ADS
        try:
            exam["exam"] = json.dumps(self.data, indent=4)
            # make a backup copy of the exam - cached version
            with open(f"app/data/{self.studentid}.json", "w") as f:
                f.write(exam["exam"])
            # create an archive of the exam before sending it off to the ADS
            with zipstream.ZipFile(mode="w", compression=zipstream.ZIP_DEFLATED) as zip:
                # zip.writestr(f"{studentid}.json", data["exam"])
                zip.write(f"app/data/{self.studentid}.json", f"{self.studentid}.json")
                with open(f"app/data/{self.studentid}.zip", "wb") as zf:
                    for _data in zip:
                        zf.write(_data)  # type: ignore[override]

            try:
                if final:
                    examstate = "closed"
                else:
                    examstate = "active"
                """
                examfile = {
                    "exam": (
                        f"app/data/{self.studentid}.{extension}",
                        open(f"app/data/{self.studentid}.{extension}", "rb"),
                        "multipart/form-data",
                    ),
                    "final": final,
                }
                #"""
                examfile = {
                    "exam": (
                        f"app/data/{self.studentid}.{extension}",
                        open(f"app/data/{self.studentid}.{extension}", "rb"),
                        "application/zip",
                    ),
                    "final": examstate,
                }
                frmdata = {"final": examstate}

                if pathlib.Path(f"app/data/{self.studentid}.{extension}").exists():
                    response = requests.post(URL, files=examfile, data=frmdata, headers=None)  # type: ignore'
                    rsp = response.json()
                    print(rsp)
                    if rsp["Status"] == "OK":
                        # if response.text == "OK":
                        return True
                    if rsp["Status"] == "Error":
                        logger.error(
                            f"Unable to upload the examination for {self.studentid}"
                        )
                        return False
            except:
                logger.error(f"Unable to upload the examination for {self.studentid}")
                return False
        except:
            logger.error(
                f"Unable to create local copy of the examination for {self.studentid}"
            )
            return False

        return False

    def getExam(self) -> bool:
        """This function communicates with the delivery server to retrieve
        the current exam.

        Args:
            None:

        Returns:
            bool: Exam was loaded if True
        """
        logger.info(
            f"Retrieving exam for {self.assessmentid} and password {self.password}"
        )
        URL = f"http://{self.URL}:8088/exam/{self.assessmentid}/{self.password}"  # "http://127.0.0.1:8088/2025S1ITCS5.100/abcd1234"
        query_parameters = {"downloadformat": "json"}

        # if os.path.exists(f"app/data/{studentid}.json"):
        if pathlib.Path(f"app/data/{Exam.studentid}.json").exists():
            logger.info(
                f" - Using cached exam {self.assessmentid} for learner {self.studentid}"
            )
            with open(f"app/data/{Exam.studentid}.json", "r") as file:
                self.data = json.load(file)
        else:
            logger.info(f" - using clean exam {self.assessmentid}")
            try:
                # retrieve the current exam from the ADS
                response = requests.get(URL, params=query_parameters)
                self.data = dict(json.loads(response.text))
            except:
                self.data = {}  # no exam to use
                logger.error(f"Requested exam, {self.assessmentid}, was not found")
                return False

        return True

    def purgeExam(self):
        """Remove the cached exam after it has been saved. Remove other exams in the process

        Args:
            None

        Returns:
        None
        """
        try:
            # remove the cached files
            if (
                self.studentid
                and pathlib.Path(f"app/data/{Exam.studentid}.json").exists()
            ):
                pathlib.Path(f"app/data/{self.studentid}.json").unlink()
            if (
                self.studentid
                and pathlib.Path(f"app/data/{Exam.studentid}.json").exists()
            ):
                pathlib.Path(f"app/data/{self.studentid}.zip").unlink()
        except:
            logger.error(f"Unable to remove the cached exam files")

    def logout(self):
        self.saveExam(True)
        self.purgeExam()
        self.sessionClear()
        # this will ensure the volatile settings match the session state
        self.sessionLoad()

    def sessionLoad(self):
        try:
            self._assessmentid = app.storage.user.get("assessmentid", "")
            self._studentid = app.storage.user.get("studentid", "")
            self._password = app.storage.user.get("password", "")
            self._authenticated = app.storage.user.get("authenticated", False)
            self._starttime = app.storage.user.get("starttime", 0)
            self._duration = app.storage.user.get("duration", 0)
        except:
            logger.warning("Unable to load the active session")

    def sessionSave(self):

        try:
            app.storage.user.update(
                {
                    "assessmentid": self._assessmentid,
                    "studentid": self._studentid,
                    "password": self._password,
                    "authenticated": self._authenticated,
                    "starttime": self._starttime,  # unix epoch time in seconds
                    "duration": self._duration,  # expected duration of the exam in minutes
                }
            )
        except:
            logger.warning("Unable to save the active session")

    def sessionClear(self):
        try:
            app.storage.user.update(
                {
                    "assessmentid": "",
                    "studentid": "",
                    "password": "",
                    "authenticated": False,
                    "starttime": 0,
                    "duration": 0,
                }
            )
        except:
            logger.warning("Unable to clear the active session")


Exam: Assessment = Assessment()
