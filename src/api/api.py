import os
import time
import httpx
import asyncio
import nest_asyncio
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_compatible_embedding
from lightrag.utils import EmbeddingFunc

from ..utils.models import *
from ..utils.utils import process_messages, append_random_hex_to_list, get_embedding_dim, stream_generator

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

# Global variables
available_models = []
app = FastAPI(title="LightRAG API", description="API for RAG operations")

# LLM and embedding functions
async def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):

    is_final_request = kwargs.get('is_final_request', False)
    frontend_model = kwargs.get('frontend_model', LLM_MODEL)

    if is_final_request:
        messages = []
        current_role = None
        current_content = []
        
        lines = prompt.split('\n')
        for line in lines:
            if line.startswith('System: '):
                if current_role:
                    messages.append({"role": current_role, "content": ' '.join(current_content)})
                current_role = "system"
                current_content = [line[8:]]
            elif line.startswith('User: '):
                if current_role:
                    messages.append({"role": current_role, "content": ' '.join(current_content)})
                current_role = "user"
                current_content = [line[6:]]
            elif line.startswith('Assistant: '):
                if current_role:
                    messages.append({"role": current_role, "content": ' '.join(current_content)})
                current_role = "assistant"
                current_content = [line[11:]]
            elif line.strip():
                if current_role:
                    current_content.append(line.strip())

        if current_role and current_content:
            messages.append({"role": current_role, "content": ' '.join(current_content)})
        
        if len(messages) > len(history_messages):
            history_messages = messages
        else:
            last_user_idx = -1
            for i, m in enumerate(messages):
                if m["role"] == "user":
                    last_user_idx = i
            if last_user_idx != -1:
                history_messages.extend(messages[last_user_idx:])
        prompt = ""
    else:
        history_messages = []
        lines = prompt.split('\n')
        last_assistant_idx = -1
        for i, line in enumerate(lines):
            if line.startswith('Assistant:'):
                if i < len(lines) - 1 and lines[i+1].startswith('User:'):
                    continue
                last_assistant_idx = i
        if last_assistant_idx != -1:
            prompt = '\n'.join(lines[:last_assistant_idx])

    return await openai_complete_if_cache(
        frontend_model, prompt, system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=API_KEY, base_url=BASE_URL, **kwargs
    )

async def embedding_func(texts: list[str]) -> np.ndarray:
    return await openai_compatible_embedding(
        texts,
        EMBEDDING_MODEL,
        api_key=API_KEY,
        base_url=BASE_URL,
    )

# Initialize RAG instance
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=llm_model_func,
    embedding_func=EmbeddingFunc(
        embedding_dim=asyncio.run(get_embedding_dim(embedding_func)),
        max_token_size=EMBEDDING_MAX_TOKEN_SIZE,
        func=embedding_func,
    ),
)

# API endpoints
@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions_endpoint(request: ChatRequest):
    try:
        await get_model_info()
        if request.model not in available_models:
            raise HTTPException(status_code=400, detail="Selected model is not available.")

        global LLM_MODEL

        user_message = None
        for msg in reversed(request.messages):
            if msg.role == "user":
                user_message = [msg.content]
                break

        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found.")

        appended_message = append_random_hex_to_list(user_message, 8)
        user_messages = "\n".join(appended_message)

        system_prompts = []
        history_messages = []
        prefill = None
        for msg in request.messages:
            if msg.role == "system":
                system_prompts.append(msg.content)
            elif msg.role in ["user", "assistant"]:
                history_messages.append({"role": msg.role, "content": msg.content})

        system_prompt = "\n".join(system_prompts)
        if history_messages and history_messages[-1]["role"] == "assistant":
            prefill = history_messages[-1]["content"]
            history_messages = history_messages[:-1]

        processed_message = process_messages(
            user_message=user_messages,
            system_prompt=system_prompt,
            history_messages=history_messages,
            prefill=prefill,
            strategy="current_only"
        )

        if request.stream:
            return StreamingResponse(
                stream_generator(rag, processed_message, system_prompt, history_messages, request.model),
                media_type="text/event-stream"
            )
        
        result = rag.query(
            processed_message,
            param=QueryParam(mode="local", only_need_context=False),
            system_prompt_from_frontend=system_prompt,
            history_messages=history_messages,
            frontend_model=request.model
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
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/models")
async def get_model_info():
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(API_port))
