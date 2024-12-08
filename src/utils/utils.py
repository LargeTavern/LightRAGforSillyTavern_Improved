import secrets
import asyncio
from typing import Optional, List, AsyncGenerator

from lightrag import QueryParam

# Global variables for LLM model management
async def stream_generator(
    rag,
    processed_message: str,
    system_prompt: Optional[str],
    history_messages: list[dict],
    frontend_model
) -> AsyncGenerator[str, None]:
    """
    Generate streaming responses from the RAG query result.
    """
    # Perform the rag.query operation
    result = rag.query(
            processed_message,
            param=QueryParam(mode="local", only_need_context=False),
            system_prompt_from_frontend=system_prompt,
            history_messages=history_messages,
            frontend_model=frontend_model
        )
    
    content_chunks = result.split()
    for chunk in content_chunks:
        yield f'data: {{"id": "chunk", "object": "chat.completion.chunk", "choices": [{{"index": 0, "delta": {{"content": "{chunk}"}}}}]}}\n\n'
        await asyncio.sleep(0.1)

    yield 'data: {"id": "done", "object": "chat.completion.chunk", "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]}\n\n'

def process_messages(
    user_message: str,
    system_prompt: Optional[str],
    history_messages: list[dict],
    prefill: Optional[str],
    strategy: str = "full_context",
) -> str:
    if strategy == "current_only":
        message = f"User: {user_message}"
        if prefill:
            message += f"\nAssistant: {prefill}"
        return message

    elif strategy == "recent_context":
        recent_messages = history_messages[-3:]
        full_context = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in recent_messages
        )
        message = f"{full_context}\nUser: {user_message}"
        if prefill:
            message += f"\nAssistant: {prefill}"
        return message

    elif strategy == "full_context":
        full_context = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in history_messages
        )
        message = f"{full_context}\nUser: {user_message}"
        if prefill:
            message += f"\nAssistant: {prefill}"
        return message

    raise ValueError(f"Unknown strategy: {strategy}")

def append_random_hex_to_list(user_messages: List[str], hex_length: int = 8) -> List[str]:
    modified_messages = []
    for message in user_messages:
        if isinstance(message, str):
            random_hex = secrets.token_hex(nbytes=hex_length // 2)
            modified_messages.append(f"{message}\n\n\n---The following strings are for markup only and are not relevant to the above, so please ignore them---\n\n\n[#{random_hex}]")
        else:
            modified_messages.append(message)
    return modified_messages

async def get_embedding_dim(embedding_func) -> int:
    test_text = ["This is a test sentence."]
    embedding = await embedding_func(test_text)
    return embedding.shape[1]