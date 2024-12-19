
# Global variables for LLM model management
def process_messages(
    history_messages: list[dict],
    strategy: str = "full_context",
):

    if strategy == "current_only":
        user_message = next(msg['content'] for msg in reversed(history_messages) if msg['role'] == 'user')
        message = f"```\n{user_message}\n```"

    elif strategy == "recent_context":
        # Find the index of the latest user message
        latest_user_idx = next(i for i, msg in enumerate(reversed(history_messages)) if msg['role'] == 'user')
        # Get 3 latest messages
        recent_messages = [msg for msg in reversed(history_messages) if msg['role'] != 'system'][(latest_user_idx):][:3]
        message = "\n".join(
            f"```\n{msg['role'].capitalize()}: {msg['content']}\n```"
            for msg in recent_messages
        )

    elif strategy == "full_context":
        message = "\n".join([
            f"```\n{msg['role'].capitalize()}: {msg['content']}\n```"
            for msg in history_messages
            if msg['role'] != 'system'
        ])

    if message:
        return message    

    raise ValueError(f"Unknown strategy: {strategy}")

async def get_embedding_dim(embedding_func) -> int:
    test_text = ["This is a test sentence."]
    embedding = await embedding_func(test_text)
    return embedding.shape[1]