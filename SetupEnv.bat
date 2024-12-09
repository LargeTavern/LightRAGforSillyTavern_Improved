@echo off
echo Welcome to the environment variable configuration tool!
echo Currently, only OpenAI models are supported directly, for other models, please use a proxy that supports OpenAI standard format responses.
echo If you want to skip a variable you can type "skip" and press the enter key!
echo.

:: Step 1: Ensure that file_DIR is not added repeatedly
setlocal enabledelayedexpansion
set /p file_DIR="Please enter the path of the folder to be used for scanning your documents (Default: ./text/book.txt; type skip to skip): "
if "%file_DIR%"=="skip" (
    echo Skip setting file_DIR
) else (
    if "%file_DIR%"=="" set file_DIR=./text/book.txt
    echo Updating the file_DIR environment variable...
    findstr /v "file_DIR=" .env > .env.tmp
    echo file_DIR=%file_DIR% >> .env.tmp
    move /Y .env.tmp .env
    echo The environment variable file_DIR has been set to: %file_DIR%
)

:: Step 2: Ensure that RAG_DIR is not added repeatedly
set /p rag_DIR="Please enter the path to the Knowledge Graph folder (Default: ./file/test; type skip to skip): "
if "%rag_DIR%"=="skip" (
    echo Skip setting RAG_DIR
) else (
    if "%rag_DIR%"=="" set rag_DIR=./file/test
    echo Updating the RAG_DIR environment variable...
    findstr /v "RAG_DIR=" .env > .env.tmp
    echo RAG_DIR=%rag_DIR% >> .env.tmp
    move /Y .env.tmp .env
    echo Environment variable RAG_DIR has been set to: %rag_DIR%
)

:: Step 3: Setup OPENAI_BASE_URL
set /p OPENAI_BASE_URL="Please enter the OpenAI API base URL (type skip to skip): "
if "%OPENAI_BASE_URL%"=="skip" (
    echo Skip setting OPENAI_BASE_URL
) else (
    echo Updating the OPENAI_BASE_URL environment variable...
    findstr /v "OPENAI_BASE_URL=" .env > .env.tmp
    echo OPENAI_BASE_URL=%OPENAI_BASE_URL% >> .env.tmp
    move /Y .env.tmp .env
    echo The environment variable OPENAI_BASE_URL is set to: %OPENAI_BASE_URL%
)

:: Step 4: Setup OPENAI_API_KEY
set /p OPENAI_API_KEY="Enter the OpenAI API key (type skip to skip): "
if "%OPENAI_API_KEY%"=="skip" (
    echo Skip setting OPENAI_API_KEY
) else (
    echo Updating the OPENAI_API_KEY environment variable...
    findstr /v "OPENAI_API_KEY=" .env > .env.tmp
    echo OPENAI_API_KEY=%OPENAI_API_KEY% >> .env.tmp
    move /Y .env.tmp .env
    echo The environment variable OPENAI_API_KEY is set to: %OPENAI_API_KEY%
)

:: Step 5: Setup LLM_MODEL
set /p LLM_MODEL="Please enter the LLM model (type skip to skip): "
if "%LLM_MODEL%"=="skip" (
    echo Skip setting LLM_MODEL
) else (
    echo Updating LLM_MODEL environment variable...
    findstr /v "LLM_MODEL=" .env > .env.tmp
    echo LLM_MODEL=%LLM_MODEL% >> .env.tmp
    move /Y .env.tmp .env
    echo Environment variable LLM_MODEL is set to: %LLM_MODEL%
)

:: Step 6: Setup KNOWLEDGE_GRAPH_MODEL
set /p KNOWLEDGE_GRAPH_MODEL="Please enter the LLM KNOWLEDGE GRAPH model (type skip to skip): "
if "%KNOWLEDGE_GRAPH_MODEL%"=="skip" (
    echo Skip setting KNOWLEDGE_GRAPH_MODEL
) else (
    echo Updating KNOWLEDGE_GRAPH_MODEL environment variable...
    findstr /v "KNOWLEDGE_GRAPH_MODEL=" .env > .env.tmp
    echo KNOWLEDGE_GRAPH_MODEL=%KNOWLEDGE_GRAPH_MODEL% >> .env.tmp
    move /Y .env.tmp .env
    echo The environment variable KNOWLEDGE_GRAPH_MODEL has been set to: %KNOWLEDGE_GRAPH_MODEL%
)

:: Step 7: Setup EMBEDDING_MODEL
set /p EMBEDDING_MODEL="Please enter the embedding model (type skip to skip): "
if "%EMBEDDING_MODEL%"=="skip" (
    echo Skip setting EMBEDDING_MODEL
) else (
    echo Updating the EMBEDDING_MODEL environment variable...
    findstr /v "EMBEDDING_MODEL=" .env > .env.tmp
    echo EMBEDDING_MODEL=%EMBEDDING_MODEL% >> .env.tmp
    move /Y .env.tmp .env
    echo The environment variable EMBEDDING_MODEL has been set to: %EMBEDDING_MODEL%
)

:: Step 8: Setup EMBEDDING_MAX_TOKEN_SIZE
set /p EMBEDDING_MAX_TOKEN_SIZE="Please enter the maximum number of tokens for the embedding model (Default: 2046; type skip to skip): "
if "%EMBEDDING_MAX_TOKEN_SIZE%"=="skip" (
    echo Skip setting EMBEDDING_MAX_TOKEN_SIZE
) else (
    if "%EMBEDDING_MAX_TOKEN_SIZE%"=="" set EMBEDDING_MAX_TOKEN_SIZE=2046
    echo Updating EMBEDDING_MAX_TOKEN_SIZE environment variable...
    findstr /v "EMBEDDING_MAX_TOKEN_SIZE=" .env > .env.tmp
    echo EMBEDDING_MAX_TOKEN_SIZE=%EMBEDDING_MAX_TOKEN_SIZE% >> .env.tmp
    move /Y .env.tmp .env
    echo The environment variable EMBEDDING_MAX_TOKEN_SIZE has been set to %EMBEDDING_MAX_TOKEN_SIZE%
)

:: Step 9: Setup API_port
set /p API_port="Please enter the service port (Default: 8020; type skip to skip): "
if "%API_port%"=="skip" (
    echo Skip setting API_port
) else (
    if "%API_port%"=="" set API_port=8020
    echo Updating the API_port environment variable...
    findstr /v "API_port=" .env > .env.tmp
    echo API_port=%API_port% >> .env.tmp
    move /Y .env.tmp .env
    echo Environment variable API_port has been set to: %API_port%
)

echo.
echo All environment variables have been set!
echo You can run Setup Your Graph.bat to build a knowledge graph, and Run API.bat when it's done or you already have a knowledge graph.
