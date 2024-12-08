@echo off
REM Setup conda
call conda activate lightrag

REM Building the Knowledge Graph
echo [Info] Running service...
python ".\src\api\api.py"
if errorlevel 1 (
    echo [Error] Failed to run the service, please check the error thrown and troubleshoot, or check the network connection.
    pause
    exit /b
)

REM Echo completion
echo [Success] Ran successfully, you can start connecting to SillyTavern!
echo [Hint] Your API port is shown below, check out the tutorial to put that URL in SillyTavern!
pause