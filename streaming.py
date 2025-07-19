from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# .stream
chat = ChatOpenAI(api_key=api_key,max_completion_tokens=200)

for item in chat.stream("yuki ishikawa"):
    print(item.content, end='✅', flush=True)

# StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI
from langchain.callbacks import StreamingStdOutCallbackHandler

llm = ChatOpenAI(
    api_key=api_key,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    max_completion_tokens=50
)

res = llm.invoke('yuki ishikawa')
print(res)