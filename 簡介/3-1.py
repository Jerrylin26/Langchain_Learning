from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(
    api_key = api_key,
    model_name = 'gpt-4.1-nano-2025-04-14',
    max_tokens=50)


# invoke方法
res = llm.invoke('你是誰')
print(res)
print(type(res))

# __call__方法
res = llm('我是學生')
print(res)
print(type(res))


# generate 方法 
res = llm.generate(
    ["請給我一則笑話"]
)
print(type(res))
print(res.llm_output)
print('----------------------')
for data in res.generations:
    print(data)
    print(type(data[0]))

print('----------------------')
print(res.model_dump())





