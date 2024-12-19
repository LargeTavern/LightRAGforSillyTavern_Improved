@echo off
chcp 65001 > nul

REM 启动新的 CMD 窗口并运行 RunAPI.bat
start "" cmd /k call .\RunAPI.bat

REM 启动新的 CMD 窗口并运行 RunWeb.bat
start "" cmd /k call .\RunWeb.bat

REM 显示提示
echo 已经启动了API 和 Web服务

exit