import os
import time
import httpx
import asyncio
import nest_asyncio
import inspect
import json
import logging
import numpy as np
import pandas as pd
import textract
import shutil
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_compatible_embedding
from lightrag.utils import EmbeddingFunc
from Gradio.graph_visual_with_html import KnowledgeGraphVisualizer as kgHTML

from src.utils.models import *
from src.utils.utils import process_messages, get_embedding_dim, get_rag_instance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Apply nest_asyncio and load environment
nest_asyncio.apply()
load_dotenv()

# Configuration
API_port = os.getenv("API_port")
WORKING_DIR = os.getenv("RAG_DIR")
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBEDDING_MAX_TOKEN_SIZE = int(os.getenv("EMBEDDING_MAX_TOKEN_SIZE"))
BASE_URL = os.getenv("OPENAI_BASE_URL")
API_KEY = os.getenv("OPENAI_API_KEY")

# Create working directory if not exists
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# File handling configuration
SUPPORTED_FILE_TYPES = ["txt", "pdf", "doc", "docx", "ppt", "pptx", "csv"]
BASE_DIR = "./text"

# Global variables
available_models = []
app = FastAPI(title="LightRAG API", description="API for RAG operations")

# LLM and embedding functions
async def llm_model_func(prompt, system_prompt=None, history_messages=[], keyword_extraction=False, frontend_model=LLM_MODEL, **kwargs):
    load_dotenv(override=True)

    if not keyword_extraction:
        prompt = ""

    return await openai_complete_if_cache(
        frontend_model, prompt, system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=API_KEY, base_url=BASE_URL, **kwargs
    )

async def embedding_func(texts: list[str]) -> np.ndarray:
    load_dotenv(override=True)

    return await openai_compatible_embedding(
        texts,
        EMBEDDING_MODEL,
        api_key=API_KEY,
        base_url=BASE_URL,
    )

# API endpoints
@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions_endpoint(request: ChatRequest):
    load_dotenv()
    rag = get_rag_instance()  # Get fresh instance here
    try:
        await get_model_info()
        if request.model not in available_models:
            raise HTTPException(status_code=400, detail="Selected model is not available.")

        system_prompts = []
        history_messages = []
        # Get only the system prompts from the front of messages
        for msg in request.messages:
            if msg.role == "system":
                system_prompts.append(msg.content)
            else:
                break  # Stop once we hit a non-system message
        
        # Get remaining messages starting from first non-system message
        history_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages[len(system_prompts):]
        ]

        system_prompt = "\n".join(system_prompts)

        processed_message = process_messages(
            history_messages=history_messages,
            strategy="current_only"
        )
        

        kwargs = {
            key: getattr(request, key)
            for key in ['temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
                   'presence_penalty', 'stop', 'top_k']
            if hasattr(request, key) and getattr(request, key) is not None
        }

        result = rag.query(
            processed_message,
            system_prompt=system_prompt,
            history_messages=history_messages,
            frontend_model=request.model,
            param=QueryParam(mode="local", only_need_context=False, stream=request.stream),
            **kwargs
        )


        if request.stream:
            if inspect.isasyncgen(result):
                async def generate():
                    async for chunk in result:
                        if isinstance(chunk, dict):
                            yield f"data: {json.dumps(chunk)}\n\n"
                        elif chunk:
                            yield f"data: {json.dumps({'choices': [{'delta': {'content': chunk}}]})}\n\n"

                return StreamingResponse(
                    generate(), 
                    media_type="text/event-stream"
                )

        created_time = int(time.time())
        return ChatCompletionResponse(
            id="completion",
            object="chat.completion",
            created=created_time,
            model=request.model,
            choices=[
                Choice(
                    index=0,
                    message=Message(role="assistant", content=result),
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=len(system_prompt.split()),
                completion_tokens=len(result.split()),
                total_tokens=len(system_prompt.split()) + len(result.split())
            )
        )

    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/v1/models")
async def get_model_info():
    load_dotenv()
    global available_models
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/models", headers=headers)
            response.raise_for_status()
            response_data = response.json()
            available_models = [model["id"] for model in response_data.get("data", [])]
            return JSONResponse(content=response.json(), status_code=response.status_code)
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="API request failed")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/v1/file", response_model=FileResponse)
async def upload_file_to_build(file: UploadFile = File(...), purpose: str = "knowledge_graph_build"):
    load_dotenv()
    rag = get_rag_instance()
    try:
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in SUPPORTED_FILE_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")
        
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        folder_name = f"{file.filename.rsplit('.', 1)[0]}_{current_time}"
        save_dir = os.path.join(BASE_DIR, folder_name)
        os.makedirs(save_dir, exist_ok=True)

        file_path = os.path.join(save_dir, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        if file_ext == "csv":
            df = pd.read_csv(file_path)
            content = df.to_string()
        else:
            content = textract.process(file_path).decode("utf-8")

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: rag.insert(content))

        return FileResponse(
            id=folder_name,
            filename=file.filename,
            purpose=purpose,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@app.post("/v1/files", response_model=FilesResponse)
async def upload_files_to_build_frontend(request: FilesRequest):
    load_dotenv(override=True)
    rag = get_rag_instance()
    responses = []

    for file_name, file_path in request.files.items():
        try:
            if not os.path.exists(file_path):
                responses.append(FilesResponse(
                    filename=file_name,
                    file_path=file_path,
                    purpose=request.purpose,
                    status="failed",
                    message="File path does not exist"
                ))
                continue

            file_ext = file_name.split(".")[-1].lower()
            if file_ext not in SUPPORTED_FILE_TYPES:
                responses.append(FilesResponse(
                    filename=file_name,
                    file_path=file_path,
                    purpose=request.purpose,
                    status="failed",
                    message=f"Unsupported file type: {file_ext}"
                ))
                continue

            if file_ext == "csv":
                df = pd.read_csv(file_path)
                content = df.to_string()
            else:
                content = textract.process(file_path).decode("utf-8")

            async def async_insert(rag, content):
                await asyncio.to_thread(rag.insert, content)

            await async_insert(rag, content)

            responses.append(FilesResponse(
                filename=file_name,
                file_path=file_path,
                purpose=request.purpose,
                status="processed",
                message="File processed successfully"
            ))

        except Exception as e:
            responses.append(FilesResponse(
                filename=file_name,
                file_path=file_path,
                purpose=request.purpose,
                status="failed",
                message=f"Failed to process file: {str(e)}"
            ))

    # Create knowledge graph visualization after processing all files
    visualizer = kgHTML(os.getenv("RAG_DIR") + f"/graph_chunk_entity_relation.graphml")
    html_file_path = visualizer.generate_graph()
    
    return JSONResponse(content=[response.dict() for response in responses])

@app.post("/v1/connect", response_model=ConnectResponse)
async def check_connection():
    return ConnectResponse(connective=True)

if __name__ == "__main__":
    import uvicorn
    rag = get_rag_instance()
    print(f"Updated RAG_DIR to: {rag.working_dir}")
    uvicorn.run(app, host="0.0.0.0", port=int(API_port))
