from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

template = '請幫我生成用{language}列印"hello world"的範例程式'
prompt_tpl = PromptTemplate.from_template(template)

llm = OpenAI(temperature=0.3, api_key=api_key,max_tokens=50)
for language_type in ['Python', 'Java', 'C#']:
    prompt = prompt_tpl.format(language=language_type)
    print(f'{"="*10}{language_type}{"="*10}')
    print(llm.invoke(prompt))
