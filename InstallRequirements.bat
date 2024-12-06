@echo off
REM Setup conda
call conda create -n lightrag
call conda activate lightrag
call conda install python=3.11 git

REM Check the Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] No valid Python installation detected, please check if the embedded Python is complete.
    pause
    exit /b
)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [Error] The file requirements.txt was not found, please make sure it exists.
    pause
    exit /b
)

REM Installing pybind11
echo [Info] Installing pybind11 with embedded Python, please wait...
pip install pybind11
if errorlevel 1 (
    echo [Error] Pybind11 installation failed, please check your network connection.
    pause
    exit /b
)

REM Installing numpy
echo [Info] Installing numpy with embedded Python, please wait...
pip install numpy
if errorlevel 1 (
    echo [Error] Numpy installation failed, please check your network connection.
    pause
    exit /b
)

REM Installing project dependencies
echo [Info] Installing project dependencies with embedded Python, please wait...
pip install -r requirements.txt
if errorlevel 1 (
    echo [Error] Dependency installation failed, please check the requirements.txt file or your network connection.
    pause
    exit /b
)

REM Installing development mode packages
echo [Info] Installing the current project in editable mode...
pip install -e .
if errorlevel 1 (
    echo [Error] Editable mode installation failed, please check the current directory and Python environment.
    pause
    exit /b
)

REM Echo completion
echo [Success] The installation is complete and the project is ready to run!
pause
