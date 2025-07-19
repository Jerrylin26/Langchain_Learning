from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
import time
from langchain_core.caches import BaseCache
from typing import Optional, Any
from langchain_core.outputs import Generation
from collections.abc import Sequence
import langchain
from langchain_openai import ChatOpenAI
from langchain.globals import set_llm_cache
from langchain.schema import HumanMessage

RETURN_VAL_TYPE = Sequence[Generation]


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class InMemoryCache(BaseCache):
    """Cache that stores things in memory."""

    def __init__(self) -> None:

        self._cache: dict[tuple[str, str], RETURN_VAL_TYPE] = {}
    
    def lookup(self, 
               prompt: str, 
               llm_string: str
               ) -> Optional[RETURN_VAL_TYPE]:

        print(f"✅[LOOKUP] prompt={prompt}, llm_string={llm_string}")
        return self._cache.get((prompt, llm_string), None)

    def update(self, 
               prompt: str, 
               llm_string: str, 
               return_val: RETURN_VAL_TYPE) -> None:

        print(f"❌[UPDATE] prompt={prompt}, llm_string={llm_string}")
        self._cache[(prompt, llm_string)] = return_val

    def clear(self, **kwargs: Any) -> None:

        self._cache = {}


# 啟用快取
cache = InMemoryCache()
set_llm_cache(cache)

# 初始化 LLM
llm = ChatOpenAI(api_key=api_key, max_completion_tokens=50)

# 用統一的 llm_string
llm_string = llm._get_llm_string()
print('--------------------')
print(llm_string)
prompt = [HumanMessage(content="賽亞超人")]

# 第一次呼叫：會觸發 lookup(), update()
start_time = time.time()
res = llm.invoke(prompt)
print(res.content)
print("🔰 check: ", llm._get_llm_string())
print("🔰🔰 check: ", prompt)
print("no cache:", time.time() - start_time)

# 第二次呼叫：會走 lookup(), 因為對應到相同prompt
start_time = time.time()
print(llm.invoke(prompt).content)
print("🔰 check: ", llm._get_llm_string())
print("🔰🔰 check: ", prompt)
print("cached:", time.time() - start_time)
