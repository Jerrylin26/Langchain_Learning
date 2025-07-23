from enum import Enum
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import EnumOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class Color(Enum):
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'
    PURPLE = 'purple'
    PINK = 'pink'

outputparser = EnumOutputParser(enum=Color)
instructions = outputparser.get_format_instructions()

print(f'instructions: {instructions}')

prompt_tpl = PromptTemplate.from_template(
    template='草地是什麼顏色.\n{instructions}回答使用英文',
    partial_variables={'instructions': instructions}
)

prompt = prompt_tpl.format()
print('✅prompt: ',prompt)

llm = OpenAI(api_key=api_key,max_tokens=50,model_name='gpt-3.5-turbo-instruct')
output = llm.invoke(prompt)
print(f'🧭output: {output}, 🧭type: {type(output)}')

output_format = outputparser.parse(response=output)
print(f'🧩output_format: {output_format}, 🧩type: {type(output_format)}')