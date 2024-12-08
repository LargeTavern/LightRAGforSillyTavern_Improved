@echo off
chcp 65001 > nul
REM 配置 conda
call conda activate lightrag

REM 启动知识图谱
echo [信息] 启动知识图谱服务...
python ".\src\api\api.py"
if errorlevel 1 (
    echo [错误] 启动服务失败，请查看抛出的错误并进行排查，或者联系管理员。
    pause
    exit /b
)

REM 显示成功信息
echo [成功] 服务启动成功，可以开始连接使用。
echo [提示] 服务的端口为，请查看文档获取详细的URL。
pause