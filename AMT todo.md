# AMT Todo & summary of changes

- AMT: link the auth to the ADS - update auth middleware handler (main.py)
  - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ 
- AMT: map out proposed routes
  - > marker
  - GET   /mark/exams/:course - return examlist for given course
  - GET   /mark/exam/:learner/:course - course optional, return all learner exams if course blank 
  - PUT   /mark/exam/:learner/:course - save the marked exam
  
  - > builder
  - GET   /build/exam/ - return list of exams
  - GET   /build/exam/:examid - retrieve exam to edit
  - POST  /build/exam/:examid - save new exam
  - PUT   /build/exam/:examid - update exam

  - > reports
  - GET /report/exams/:filter - exams in the system
  - GET /report/course/:filter - exams by course
  - GET /report/learner/:filter - grades by learner
  - 

### other

**LOC counter**
Get-ChildItem -recurse *.go |Get-Content | Measure-Object -line

