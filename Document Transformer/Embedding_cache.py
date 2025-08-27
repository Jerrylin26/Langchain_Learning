from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import InMemoryStore, LocalFileStore
from dotenv import load_dotenv
import os
import time


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

embeddings_model = OpenAIEmbeddings(api_key=api_key)

def calculate_embed_time(embedder):
    start = time.time()
    embedder.embed_documents(['hello','goodbye'])
    return time.time() - start


underlying_embeddings = OpenAIEmbeddings()

# 使用記憶體快取
store = InMemoryStore()
embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,store,namespace=underlying_embeddings.model
)

print(f'memory - no cache: {calculate_embed_time(embedder)}')
print(f'memory - cache: {calculate_embed_time(embedder)}')


# 使用檔案快取
store = LocalFileStore('./Document Transformer/embedding_cache/')
embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,store,namespace=underlying_embeddings.model
)

print(f'memory - no cache: {calculate_embed_time(embedder)}')
print(f'memory - cache: {calculate_embed_time(embedder)}')


