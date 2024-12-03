@echo off
echo 欢迎使用环境变量配置工具！
echo 目前仅直接支持OpenAI模型，其他模型请使用中转系统来支持OpenAI标准格式的响应
echo 想要跳过某个变量的话可以输入skip，直接回车会输入空字符！！！
echo.

:: Step 1: 确保没有重复添加 file_DIR
setlocal enabledelayedexpansion
set /p file_DIR="): "请输入待使用的文本文件夹路径 (默认 ./text/book.txt，输入 skip 跳过:)"
if "%file_DIR%"=="skip" (
    echo 跳过设置 file_DIR
) else (
    if "%file_DIR%"=="" set file_DIR=./text/book.txt
    echo 正在更新 file_DIR 环境变量...
    findstr /v "file_DIR=" .env > .env.tmp
    echo file_DIR=%file_DIR% >> .env.tmp
    move /Y .env.tmp .env
    echo 环境变量 file_DIR 已设置为：%file_DIR%
)

:: Step 2: 确保没有重复添加 RAG_DIR
set /p rag_DIR="请输入知识图谱文件夹路径 (默认 ./file/test，输入 skip 跳过:) "
if "%rag_DIR%"=="skip" (
    echo 跳过设置 RAG_DIR
) else (
    if "%rag_DIR%"=="" set rag_DIR=./file/test
    echo 正在更新 RAG_DIR 环境变量...
    findstr /v "RAG_DIR=" .env > .env.tmp
    echo RAG_DIR=%rag_DIR% >> .env.tmp
    move /Y .env.tmp .env
    echo 环境变量 RAG_DIR 已设置为：%rag_DIR%
)

:: Step 3: 引导用户输入 OPENAI_BASE_URL
set /p OPENAI_BASE_URL="请输入 OpenAI API 基础 URL (输入 skip 跳过): "
if "%OPENAI_BASE_URL%"=="skip" (
    echo 跳过设置 OPENAI_BASE_URL
) else (
    echo 正在更新 OPENAI_BASE_URL 环境变量...
    findstr /v "OPENAI_BASE_URL=" .env > .env.tmp
    echo OPENAI_BASE_URL=%OPENAI_BASE_URL% >> .env.tmp
    move /Y .env.tmp .env
    echo 环境变量 OPENAI_BASE_URL 已设置为：%OPENAI_BASE_URL%
)

:: Step 4: 引导用户输入 OPENAI_API_KEY
set /p OPENAI_API_KEY="请输入 OpenAI API 密钥 (输入 skip 跳过): "
if "%OPENAI_API_KEY%"=="skip" (
    echo 跳过设置 OPENAI_API_KEY
) else (
    echo 正在更新 OPENAI_API_KEY 环境变量...
    findstr /v "OPENAI_API_KEY=" .env > .env.tmp
    echo OPENAI_API_KEY=%OPENAI_API_KEY% >> .env.tmp
    move /Y .env.tmp .env
    echo 环境变量 OPENAI_API_KEY 已设置为：%OPENAI_API_KEY%
)

:: Step 5: 引导用户输入 LLM_MODEL
set /p LLM_MODEL="请输入 LLM 模型 (输入 skip 跳过): "
if "%LLM_MODEL%"=="skip" (
    echo 跳过设置 LLM_MODEL
) else (
    echo 正在更新 LLM_MODEL 环境变量...
    findstr /v "LLM_MODEL=" .env > .env.tmp
    echo LLM_MODEL=%LLM_MODEL% >> .env.tmp
    move /Y .env.tmp .env
    echo 环境变量 LLM_MODEL 已设置为：%LLM_MODEL%
)

:: Step 6: 引导用户输入 EMBEDDING_MODEL
set /p EMBEDDING_MODEL="请输入嵌入模型 (输入 skip 跳过): "
if "%EMBEDDING_MODEL%"=="skip" (
    echo 跳过设置 EMBEDDING_MODEL
) else (
    echo 正在更新 EMBEDDING_MODEL 环境变量...
    findstr /v "EMBEDDING_MODEL=" .env > .env.tmp
    echo EMBEDDING_MODEL=%EMBEDDING_MODEL% >> .env.tmp
    move /Y .env.tmp .env
    echo 环境变量 EMBEDDING_MODEL 已设置为：%EMBEDDING_MODEL%
)

:: Step 7: 引导用户输入 EMBEDDING_MAX_TOKEN_SIZE
set /p EMBEDDING_MAX_TOKEN_SIZE="请输入嵌入模型最大tokens数量 (默认 2046，输入 skip 跳过): "
if "%EMBEDDING_MAX_TOKEN_SIZE%"=="skip" (
    echo 跳过设置 EMBEDDING_MAX_TOKEN_SIZE
) else (
    if "%EMBEDDING_MAX_TOKEN_SIZE%"=="" set EMBEDDING_MAX_TOKEN_SIZE=2046
    echo 正在更新 EMBEDDING_MAX_TOKEN_SIZE 环境变量...
    findstr /v "EMBEDDING_MAX_TOKEN_SIZE=" .env > .env.tmp
    echo EMBEDDING_MAX_TOKEN_SIZE=%EMBEDDING_MAX_TOKEN_SIZE% >> .env.tmp
    move /Y .env.tmp .env
    echo 环境变量 EMBEDDING_MAX_TOKEN_SIZE 已设置为：%EMBEDDING_MAX_TOKEN_SIZE%
)

:: Step 8: 引导用户输入 API_port
set /p API_port="请输入服务端口 (默认 8020，输入 skip 跳过): "
if "%API_port%"=="skip" (
    echo 跳过设置 API_port
) else (
    if "%API_port%"=="" set API_port=8020
    echo 正在更新 API_port 环境变量...
    findstr /v "API_port=" .env > .env.tmp
    echo API_port=%API_port% >> .env.tmp
    move /Y .env.tmp .env
    echo 环境变量 API_port 已设置为：%API_port%
)

echo.
echo 所有环境变量已设置完毕！
echo 可运行Setup Your Graph.bat以进行知识图谱的构建，构建完毕或者已经有知识图谱则可以运行Run API.bat
