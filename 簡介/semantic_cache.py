import time
import redis
import langchain
from langchain_openai import OpenAI, OpenAIEmbeddings, ChatOpenAI
from langchain_community.cache import RedisSemanticCache
from langchain.globals import set_llm_cache
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


set_llm_cache(RedisSemanticCache(
    redis_url="redis://localhost:6379", 
    embedding=OpenAIEmbeddings(),
    score_threshold= 0.4
))

llm = OpenAI(api_key=api_key,max_tokens=50,model='gpt-4.1-nano-2025-04-14')

start_time = time.time()
print(llm.invoke('超級賽亞人').content)
print('no cache: ', time.time() - start_time)

start_time = time.time()
print(llm.invoke('超級賽亞人是什麼').content)
print('cached: ', time.time() - start_time)

