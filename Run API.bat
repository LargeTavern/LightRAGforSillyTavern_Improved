@echo off
REM 设置嵌入的 Python 解释器路径
set PYTHON_PATH=.\python\python.exe

REM 构建知识图谱
echo [信息] 正在构建知识图谱...
"%PYTHON_PATH%" lightrag_api_openai_compatible.py
if errorlevel 1 (
    echo [错误] 运行服务失败，请查看抛出的错误并进行排查，或者检查网络连接。
    pause
    exit /b
)

REM 提示完成
echo [成功] 运行成功，可开始连接酒馆！
echo [提示] 你的服务端口为，查看README以在酒馆中填入该URL
pause