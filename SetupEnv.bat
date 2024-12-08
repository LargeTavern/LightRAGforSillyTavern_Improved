@echo off
chcp 65001 > nul
echo 欢迎使用环境设置配置工具！
echo 目前仅直接支持OpenAI模型，其他模型请使用可转系统且支持OpenAI标准格式的中转应用
echo 如要跳过某项配置的话，输入skip或直接回车即可跳过该项配置。
echo.

:: Step 1: 确保没有重复设置 file_DIR
setlocal enabledelayedexpansion
set /p file_DIR="请输入将使用的文本文件的路径 (默认 ./text/book.txt，输入 skip 跳过): "
if "%file_DIR%"=="skip" (
    echo 已跳过设置 file_DIR
) else (
    if "%file_DIR%"=="" set file_DIR=./text/book.txt
    echo 正在更新 file_DIR 环境变量...
    findstr /v "file_DIR=" .env > .env.tmp
    echo file_DIR=%file_DIR% >> .env.tmp
    move /Y .env.tmp .env
    echo 已完成设置 file_DIR ，设置为：%file_DIR%
)

:: Step 2: 确保没有重复设置 RAG_DIR
set /p rag_DIR="请输入知识图谱文件夹路径 (默认 ./file/test，输入 skip 跳过): "
if "%rag_DIR%"=="skip" (
    echo 已跳过设置 RAG_DIR
) else (
    if "%rag_DIR%"=="" set rag_DIR=./file/test
    echo 正在更新 RAG_DIR 环境变量...
    findstr /v "RAG_DIR=" .env > .env.tmp
    echo RAG_DIR=%rag_DIR% >> .env.tmp
    move /Y .env.tmp .env
    echo 已完成设置 RAG_DIR ，设置为：%rag_DIR%
)

:: Step 3: 设置用户输入 OPENAI_BASE_URL
set /p OPENAI_BASE_URL="请输入 OpenAI API 基础 URL (输入 skip 跳过): "
if "%OPENAI_BASE_URL%"=="skip" (
    echo 已跳过设置 OPENAI_BASE_URL
) else (
    echo 正在更新 OPENAI_BASE_URL 环境变量...
    findstr /v "OPENAI_BASE_URL=" .env > .env.tmp
    echo OPENAI_BASE_URL=%OPENAI_BASE_URL% >> .env.tmp
    move /Y .env.tmp .env
    echo 已完成设置 OPENAI_BASE_URL ，设置为：%OPENAI_BASE_URL%
)

:: Step 4: 设置用户输入 OPENAI_API_KEY
set /p OPENAI_API_KEY="请输入 OpenAI API 密钥 (输入 skip 跳过): "
if "%OPENAI_API_KEY%"=="skip" (
    echo 已跳过设置 OPENAI_API_KEY
) else (
    echo 正在更新 OPENAI_API_KEY 环境变量...
    findstr /v "OPENAI_API_KEY=" .env > .env.tmp
    echo OPENAI_API_KEY=%OPENAI_API_KEY% >> .env.tmp
    move /Y .env.tmp .env
    echo 已完成设置 OPENAI_API_KEY ，设置为：%OPENAI_API_KEY%
)

:: Step 5: 设置用户输入 LLM_MODEL
set /p LLM_MODEL="请输入 LLM 模型 (输入 skip 跳过): "
if "%LLM_MODEL%"=="skip" (
    echo 已跳过设置 LLM_MODEL
) else (
    echo 正在更新 LLM_MODEL 环境变量...
    findstr /v "LLM_MODEL=" .env > .env.tmp
    echo LLM_MODEL=%LLM_MODEL% >> .env.tmp
    move /Y .env.tmp .env
    echo 已完成设置 LLM_MODEL ，设置为：%LLM_MODEL%
)

:: Step 6: 设置用户输入 EMBEDDING_MODEL
set /p EMBEDDING_MODEL="请输入嵌入模型 (输入 skip 跳过): "
if "%EMBEDDING_MODEL%"=="skip" (
    echo 已跳过设置 EMBEDDING_MODEL
) else (
    echo 正在更新 EMBEDDING_MODEL 环境变量...
    findstr /v "EMBEDDING_MODEL=" .env > .env.tmp
    echo EMBEDDING_MODEL=%EMBEDDING_MODEL% >> .env.tmp
    move /Y .env.tmp .env
    echo 已完成设置 EMBEDDING_MODEL ，设置为：%EMBEDDING_MODEL%
)

:: Step 7: 设置用户输入 EMBEDDING_MAX_TOKEN_SIZE
set /p EMBEDDING_MAX_TOKEN_SIZE="请输入嵌入模型最大tokens长度 (默认 2046，输入 skip 跳过): "
if "%EMBEDDING_MAX_TOKEN_SIZE%"=="skip" (
    echo 已跳过设置 EMBEDDING_MAX_TOKEN_SIZE
) else (
    if "%EMBEDDING_MAX_TOKEN_SIZE%"=="" set EMBEDDING_MAX_TOKEN_SIZE=2046
    echo 正在更新 EMBEDDING_MAX_TOKEN_SIZE 环境变量...
    findstr /v "EMBEDDING_MAX_TOKEN_SIZE=" .env > .env.tmp
    echo EMBEDDING_MAX_TOKEN_SIZE=%EMBEDDING_MAX_TOKEN_SIZE% >> .env.tmp
    move /Y .env.tmp .env
    echo 已完成设置 EMBEDDING_MAX_TOKEN_SIZE ，设置为：%EMBEDDING_MAX_TOKEN_SIZE%
)

:: Step 8: 设置用户输入 API_port
set /p API_port="请输入端口 (默认 8020，输入 skip 跳过): "
if "%API_port%"=="skip" (
    echo 已跳过设置 API_port
) else (
    if "%API_port%"=="" set API_port=8020
    echo 正在更新 API_port 环境变量...
    findstr /v "API_port=" .env > .env.tmp
    echo API_port=%API_port% >> .env.tmp
    move /Y .env.tmp .env
    echo 已完成设置 API_port ，设置为：%API_port%
)

echo.
echo 所有环境变量设置完成！
echo 请运行SetupRAG.bat以进行知识图谱的构建，若配置完毕或已有知识图，请运行Start.bat
