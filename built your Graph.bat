@echo off
REM Setup conda
call conda activate lightrag

REM Building the Knowledge Graph
echo [Info] Building a knowledge graph...
python ".\built your Graph.py"
if errorlevel 1 (
    echo [Error] Building the Knowledge Graph failed, check the error thrown and troubleshoot, or check your network connection.
    pause
    exit /b
)

REM Echo completion
echo [Success] The build is complete and you can start running the API!
pause