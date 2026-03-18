@echo off
:: https://gregoryszorc.com/docs/python-build-standalone/main/index.html
setlocal
cd /D "%~dp0"
echo Starting in %~dp0
"%~dp0\python\python" -s "%~dp0\app\main.py"
::"%~dp0\python\python" -s "%~dp0\testing.py"

exit
::%BASE%r3dfox\r3dfox.exe http://127.0.0.1:8080

