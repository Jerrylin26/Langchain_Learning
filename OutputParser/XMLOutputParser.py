from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import XMLOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


outputparser = XMLOutputParser(
    tags=['foods', 'food', 'name', 'country', 'cost']
)
instructions = outputparser.get_format_instructions()

print(f'instructions: {instructions}')

prompt_tpl = PromptTemplate.from_template(
    template='請列舉兩個世界上最好吃的甜點.\n{instructions}',
    partial_variables={'instructions': instructions}
)

prompt = prompt_tpl.format()
print('✅prompt: ',prompt)

llm = OpenAI(api_key=api_key,max_tokens=200,model_name='gpt-3.5-turbo-instruct')
output = llm.invoke(prompt)
print(f'🧭output: {output}, 🧭type: {type(output)}')

output_format = outputparser.parse(output)
print(f'🧩output_format: ')

for food in output_format['foods']:
    print(food)