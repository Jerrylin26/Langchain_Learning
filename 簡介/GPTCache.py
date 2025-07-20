import hashlib
import time
from gptcache.manager.factory import manager_factory
from gptcache.processor.pre import get_prompt
from gptcache import Cache
from langchain_community.cache import GPTCache
from langchain.globals import set_llm_cache
import langchain
from langchain_openai import ChatOpenAI, OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


'''
def get_hashed_name(name):
    return hashlib.sha256(name.encode()).hexdigest()


## 精確匹配
def init_gptcache(cache_obj: Cache, llm: str):
    hashed_llm = get_hashed_name(llm)
    cache_obj.init(
        pre_embedding_func=get_prompt,
        data_manager=manager_factory(manager="map", data_dir=f"map_cache_{hashed_llm}"),
    )

# 這裡的內部邏輯值得學習
set_llm_cache(GPTCache(init_gptcache))

llm = ChatOpenAI(api_key=api_key, max_completion_tokens=50, model='gpt-4.1-nano-2025-04-14')


start_time = time.time()
print(llm.invoke('什麼是AI').content)
print('no cache: ', time.time() - start_time)

start_time = time.time()
print(llm.invoke('什麼是AI').content)
print('cached: ', time.time() - start_time)

start_time = time.time()
print(llm.invoke('請問,什麼是AI').content)
print('no cached: ', time.time() - start_time)
'''



## 相似匹配
from gptcache.adapter.api import init_similar_cache
from gptcache.embedding import OpenAI as OpenAIEmbedding
print(api_key)
def init_gptcache_embedding(cache_obj: Cache, llm: str):
    init_similar_cache(
        cache_obj= cache_obj,
        embedding=OpenAIEmbedding(api_key=api_key)
    )
set_llm_cache(GPTCache(init_gptcache_embedding))

llm = ChatOpenAI(api_key=api_key, max_completion_tokens=50, model='gpt-4.1-nano-2025-04-14')
api_base = os.getenv("OPENAI_API_BASE")
print(api_base)

start_time = time.time()
print(llm.invoke('超級龍珠'))
print('no cache: ', time.time() - start_time)

start_time = time.time()
print(llm.invoke('超級龍珠'))
print('cached: ', time.time() - start_time)

start_time = time.time()
print(llm.invoke('超級龍珠 賽亞超人'))
print('no cached: ', time.time() - start_time)
