@echo off
chcp 65001 > nul
REM 配置 conda
call conda create -n lightrag
call conda activate lightrag
call conda install python=3.11 git

set ENV_PATH=.\.env

REM 运行前检查
echo [信息] 正在检查运行前环境...
python ".\src\web\gradio.py"
if errorlevel 1 (
    echo [错误] 运行前检查失败，请查看抛出的错误并进行修正。
    pause
    exit /b
)

REM 显示成功信息
echo [成功] 环境检查成功，可以开始使用。
pause