@echo off
chcp 65001 > nul
REM 配置 conda
call conda activate lightrag

REM 构建知识图谱
echo [信息] 正在构建知识图谱...
python ".\src\scripts\build_graph.py"
if errorlevel 1 (
    echo [错误] 构建知识图谱失败，请查看抛出的错误并进行排查，或者联系管理员。
    pause
    exit /b
)

REM 显示提示
echo [成功] 构建完成，可以开始后续操作。
pause