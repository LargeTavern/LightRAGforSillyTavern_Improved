@echo off
chcp 65001 > nul
REM 配置 conda
call conda create -n lightrag
call conda activate lightrag
call conda install python=3.11 git

REM 启动服务
echo [信息] 正在启动服务...
python ".\src\web\api.py"
if errorlevel 1 (
    echo [错误] 服务启动失败，请查看抛出的错误并进行调试。
    pause
    exit /b
)

REM 显示成功信息
echo [成功] 服务启动成功，可以开始使用。
pause
