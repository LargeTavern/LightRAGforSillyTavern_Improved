import asyncio
import os

import numpy as np
from dotenv import load_dotenv

from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_compatible_embedding
from lightrag.utils import EmbeddingFunc

from src.utils.utils import get_embedding_dim

load_dotenv()

#你的知识图谱存放的文件夹
WORKING_DIR = os.getenv("RAG_DIR")
print(f"WORKING_DIR: {WORKING_DIR}")

#你的文档，例如./book.txt，建议存放在text这个文件夹以便管理
file_DIR = os.getenv("file_DIR")
print(f"file_DIR: {file_DIR}")

KNOWLEDGE_GRAPH_MODEL = os.getenv("KNOWLEDGE_GRAPH_MODEL")
print(f"KNOWLEDGE_GRAPH_MODEL: {KNOWLEDGE_GRAPH_MODEL}")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
print(f"EMBEDDING_MODEL: {EMBEDDING_MODEL}")
EMBEDDING_MAX_TOKEN_SIZE = int(os.getenv("EMBEDDING_MAX_TOKEN_SIZE"))
print(f"EMBEDDING_MAX_TOKEN_SIZE: {EMBEDDING_MAX_TOKEN_SIZE}")

BASE_URL=os.getenv("OPENAI_BASE_URL")
API_KEY = os.getenv("OPENAI_API_KEY")

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def llm_model_func(prompt, system_prompt=None, history_messages=[], keyword_extraction=False, frontend_model=KNOWLEDGE_GRAPH_MODEL, **kwargs) -> str:
    return await openai_complete_if_cache(
        frontend_model,
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=API_KEY,
        base_url=BASE_URL,
        **kwargs,
    )


async def embedding_func(texts: list[str]) -> np.ndarray:
    return await openai_compatible_embedding(
        texts,
        model=EMBEDDING_MODEL,
        api_key=API_KEY,
        base_url=BASE_URL,
    )


async def main():
    try:
        embedding_dimension = await get_embedding_dim(embedding_func)
        print(f"Detected embedding dimension: {embedding_dimension}")

        rag = LightRAG(
            working_dir=WORKING_DIR,
            llm_model_func=llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=embedding_dimension,
                max_token_size=EMBEDDING_MAX_TOKEN_SIZE,
                func=embedding_func,
            ),
        )


        # Check if file_DIR is a directory
        if os.path.isdir(file_DIR):
            log_file = os.path.join(file_DIR, "_DO_NOT_REMOVE_processed_files.log")
            processed_files = set()
            
            # Load processed files from log if it exists
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as log:
                    processed_files = set(log.read().splitlines())

            # Iterate through all files in the directory
            # Create a list to store all texts
            texts_to_insert = []
            files_to_log = []
            
            for filename in os.listdir(file_DIR):
                file_path = os.path.join(file_DIR, filename)
                # Skip if file was already processed or is the log file
                if filename in processed_files or filename == "_DO_NOT_REMOVE_processed_files.log":
                    print(f"Skipping already processed file: {filename}")
                    continue
                
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
                            print(f"Processing file: {filename}")
                            texts_to_insert.append(f.read())
                            files_to_log.append(filename)
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")
            
            if texts_to_insert:
                # Batch insert all texts
                await rag.ainsert(texts_to_insert)
                # Log all successfully processed files
                with open(log_file, "a", encoding="utf-8") as log:
                    log.write("\n".join(files_to_log) + "\n")
        else:
            # If file_DIR is a single file
            with open(file_DIR, "r", encoding="utf-8", errors='ignore') as f:
                await rag.ainsert(f.read())


        '''
        # Perform naive search
        print(
            await rag.aquery(
                "What is the information being told here?", param=QueryParam(mode="naive")
            )
        )

        # Perform local search
        print(
            await rag.aquery(
                "What is the information being told here?", param=QueryParam(mode="local")
            )
        )

        # Perform global search
        print(
            await rag.aquery(
                "What is the information being told here?", param=QueryParam(mode="global"),
            )
        )

        '''
        # Perform hybrid search
        print(
            await rag.aquery(
                "What is the information being told here?", param=QueryParam(mode="hybrid"),
            )
        )
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
