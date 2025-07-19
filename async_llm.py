import time
import asyncio
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def generate_serial():
    llm = ChatOpenAI(api_key=api_key, max_completion_tokens=50)
    for _ in range(12):
        res = llm.generate(messages=[[HumanMessage(content='大谷翔平')]])
        print(res.generations[0][0].text)


async def generate_async(llm):
    res = await llm.agenerate(messages=[[HumanMessage(content='日本排球國手高僑藍')]])
    print(res.generations[0][0].text)

async def generate_concurrent():
    llm = ChatOpenAI(api_key=api_key, max_completion_tokens=50)
    tasks = [generate_async(llm) for _ in range(12)]
    await asyncio.gather(*tasks)


start = time.perf_counter()
asyncio.run(generate_concurrent())
print(f'Concurrent: {(time.perf_counter() - start):0.2f} seconds.')

start = time.perf_counter()
generate_serial()
print(f'Serial: {(time.perf_counter() - start):0.2f} seconds.')

