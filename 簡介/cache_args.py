import langchain
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain_openai import ChatOpenAI, OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

set_llm_cache(InMemoryCache())

chat_llm = ChatOpenAI(api_key=api_key,cache=False)
llm = OpenAI(api_key=api_key, cache=False)