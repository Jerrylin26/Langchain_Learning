from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
import time

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# 記憶體快取
import langchain
from langchain_community.cache import InMemoryCache
from langchain_openai import ChatOpenAI
import time

langchain.globals._llm_cache = InMemoryCache()

llm = ChatOpenAI(api_key=api_key)


start_time = time.time()
print(llm.invoke('你是誰').content)
print('no cache: ', time.time() - start_time)

start_time = time.time()
print(llm.invoke('你是誰').content)
print('cached: ', time.time() - start_time)

print(langchain.globals.__cached__)


# SQLite cache
import langchain
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path="/home/jerry/code/Langchain_大型ReAct/簡介/langchain.db"))

llm = ChatOpenAI(api_key=api_key,max_completion_tokens=50)

start_time = time.time()
print(llm.invoke('保客家111').content)
print('no cache: ', time.time() - start_time)

start_time = time.time()
print(llm.invoke('保客家111').content)
print('cached: ', time.time() - start_time)

print(llm._get_llm_string())

from langchain.globals import get_llm_cache

cache = get_llm_cache()
prompt = '保客家111'
# 檢查是否是 SQLiteCache 並列出檔案路徑
print(cache.lookup(prompt,llm._get_llm_string()))

prompt = "保客家"
llm_string = llm._get_llm_string()

print("Prompt repr:", repr(prompt))
print("LLM string:", llm_string)

result = cache.lookup(prompt, llm_string)
print("Result:", result)


# SQL快取 
# 未下載SQLclient
import langchain
from sqlalchemy import create_engine
from langchain_community.cache import SQLAlchemyCache
from langchain.globals import set_llm_cache

engine = create_engine(
    "mysql+mysqldb://Jerry:lccJerry1@localhost/landchain_mysql",
    pool_recycle=3600,
    echo=True,
)


set_llm_cache(SQLAlchemyCache(engine))


llm = ChatOpenAI(api_key=api_key,max_completion_tokens=50)

start_time = time.time()
print(llm.invoke('保客家111').content)
print('no cache: ', time.time() - start_time)

start_time = time.time()
print(llm.invoke('保客家111').content)
print('cached: ', time.time() - start_time)


# Redis 快取
# 為下載redisclient
import langchain
from redis import Redis
from langchain_community.cache import RedisCache
from langchain.globals import set_llm_cache

set_llm_cache(RedisCache(redis_=Redis()))

llm = ChatOpenAI(api_key=api_key,max_completion_tokens=50)

start_time = time.time()
print(llm.invoke('超級賽亞人').content)
print('no cache: ', time.time() - start_time)

start_time = time.time()
print(llm.invoke('超級賽亞人').content)
print('cached: ', time.time() - start_time)