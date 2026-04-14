# AMT Todo & summary of changes


Assumes the ADS4 server is running with preloaded data
- Courses
- Offerings
- Learners
- Learner offerings


Need to include faculty/academic role to only show relevant exams for the logged in marker - use Offerings(Ownerid)

- AMT: link the auth to the ADS - update auth middleware handler (main.py)
  - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ 
- AMT: map out proposed routes
  - > Builder
    - New exam: (local) Create a new exam with the option to copy existing exam
    - Manage exams: (local) Edit/update any existing exams. (remote) Publish exam to server.
    - Archive exams: (remote) Toggle exam status 'active'/'closed'
  
  - Builder Routes
    - GET   /build/exam/ - return list of exams
    - GET   /build/exam/:examid - retrieve exam to edit
    - POST  /build/exam/:examid - save new exam
    - PUT   /build/exam/:examid - update exam

  - > Marker
    - List Unmarked: (remote) Show all unmarked exams by course. (remote) Includes bulk download by course.
    - Premark Exams: (local) Iterate over active exams, automarkmark then set status 'closed'->'premark', premark types MC,OWA,MAW,TF
    - Manual Mark: (local) manually mark all of the premarked exams - types SA & DI
    - Backup: (remote) backup the marked exams to the server
  - Marker routes
    - GET   /mark/exams/:course - return examlist for given course
    - GET   /mark/exam/:learner/:course - course optional, return all learner exams if course blank 
    - PUT   /mark/exam/:learner/:course - save the marked exam
    
  - > Reports(remote)
    - Current Exams: (remote) list all of the active exams in the system (not learner exams)
    - Exams by Course: (local) List learner exams by course
    - Grades by Learner: (remote) List all of the exam grades per learner - toggle exam monitoring comments
  - Reporting routes
    - GET /report/exams/:filter - exams in the system
    - GET /report/course/:filter - exams by course
    - GET /report/learner/:filter - grades by learner
  - Admin
    - Refresh course lists (remote > local)
    - Server settings (local)
    - Change passwords (remote)

- add code to create the data/[year]/[semester] for the examination

### Question types

Current list of possible question types:

  - **MC** - multi-choice. Question followed by a list of possible answers . Acronyms included.
  - **OWA** - one word answer/Fill in the blanks. Sentence with question or blank space/s for one or more words
  - **MAW** - Match a word/phrase with a statement 
  - **TF** - true/false. Simple question/statements
  - **SA** - short answer, 
  - **DI** - discussion
  - **DND** - drag-n-drop (_not implemented_), 
  - **MTP** - match the picture (_not implemented_)


### other

**LOC counter**
Get-ChildItem -recurse *.go |Get-Content | Measure-Object -line

