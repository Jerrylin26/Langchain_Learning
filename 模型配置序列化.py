from langchain_openai import OpenAI,ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(api_key=api_key, max_tokens=50)
llm.save("llm.json")

# 匯入.json 建立LLM
from langchain_community.llms.loading import load_llm

llm = load_llm('llm.json')
print(type(llm))


# 查詢load_llm() 哪些模型可用
from langchain_community.llms import get_type_to_cls_dict

print(f'model count: {len(get_type_to_cls_dict())}')
for name, model in get_type_to_cls_dict().items():
    print(f'name: {name}, model: {model}')

