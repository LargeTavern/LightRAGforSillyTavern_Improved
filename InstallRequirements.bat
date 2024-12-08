@echo off
chcp 65001 > nul
REM 配置 conda
call conda create -n lightrag
call conda activate lightrag
call conda install python=3.11 git

REM 检测 Python 版本
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到有效的 Python 安装，请检查嵌入式 Python 是否完整。
    pause
    exit /b
)

REM 检测 requirements.txt 是否存在
if not exist "requirements.txt" (
    echo [错误] 未找到 requirements.txt 文件，请确保文件存在。
    pause
    exit /b
)


REM 安装 pybind11
echo [信息] 正在使用嵌入式 Python 安装 pybind11，请稍候...
pip install pybind11
if errorlevel 1 (
    echo [错误] Pybind11 安装失败，请检查网络连接。
    pause
    exit /b
)

REM 安装 numpy
echo [信息] 正在使用嵌入式 Python 安装 numpy，请稍候...
pip install numpy
if errorlevel 1 (
    echo [错误] Numpy 安装失败，请检查网络连接。
    pause
    exit /b
)

REM 安装项目依赖
echo [信息] 正在安装项目依赖，请稍候...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败，请检查 requirements.txt 文件和网络连接。
    pause
    exit /b
)

REM 安装可编辑模式中
echo [信息] 正在以可编辑模式安装当前项目...
pip install -e .
if errorlevel 1 (
    echo [错误] 可编辑模式安装失败，请检查当前目录和 Python 环境。
    pause
    exit /b
)

REM 显示完成
echo [成功] 安装完成，项目已准备就绪！
pause
