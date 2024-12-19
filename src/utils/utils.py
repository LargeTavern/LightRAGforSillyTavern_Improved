# Global variables for LLM model management
def process_messages(
    history_messages: list[dict],
    strategy: str = "full_context",
):

    if strategy == "current_only":
        user_message = next(msg['content'] for msg in reversed(history_messages) if msg['role'] == 'user')
        message = f"User: {user_message}"

        return f"""
        ```
        {message}
        ```
        """

    elif strategy == "recent_context":
        # Find the index of the latest user message
        latest_user_idx = next(i for i, msg in enumerate(reversed(history_messages)) if msg['role'] == 'user')
        # Get 3 latest messages
        recent_messages = [msg for msg in reversed(history_messages) if msg['role'] != 'system'][(latest_user_idx):][:3]
        message = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in recent_messages
        )

        return f"""
        ```
        {message}
        ```
        """

    elif strategy == "full_context":
        message = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in history_messages
            if msg['role'] != 'system'
        ])

        return f"""
        ```
        {message}
        ```
        """        

    raise ValueError(f"Unknown strategy: {strategy}")

async def get_embedding_dim(embedding_func) -> int:
    test_text = ["This is a test sentence."]
    embedding = await embedding_func(test_text)
    return embedding.shape[1]

def get_rag_instance():
    '''
    Initialize RAG instance with current environment variables
    '''
    from lightrag import LightRAG
    from lightrag.utils import EmbeddingFunc
    import os
    import asyncio
    from dotenv import load_dotenv
    
    load_dotenv(override=True)

    rag_dir = os.getenv("RAG_DIR")
    embedding_max_tokens = int(os.getenv("EMBEDDING_MAX_TOKEN_SIZE"))

    # Get llm_model_func from api.py scope
    from src.web.api import llm_model_func, embedding_func
    
    print(f"RAG_DIR is set to: {rag_dir}")
    
    # Create RAG instance with latest env vars
    rag = LightRAG(
        working_dir=rag_dir,
        llm_model_func=llm_model_func,
        embedding_func=EmbeddingFunc(
            embedding_dim=asyncio.run(get_embedding_dim(embedding_func)),
            max_token_size=embedding_max_tokens,
            func=embedding_func,
        ),
    )
    return rag