# Package initialization
from .models import (
    QueryRequest, InsertRequest, Response,
    Message, ChatRequest, Choice, Usage, ChatCompletionResponse
)
from .utils import process_messages, append_random_hex_to_list, get_embedding_dim