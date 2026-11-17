@echo off
pushd "%~dp0"
"%~dp0.venv\Scripts\python.exe" -m terminal.ui.application %*
set "terminalExit=%errorlevel%"
popd
exit /b %terminalExit%
