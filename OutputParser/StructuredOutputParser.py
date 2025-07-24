from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

response_schemas = [

    ResponseSchema(
        name='answer',
        description='提問時的回答'
    ),
    ResponseSchema(
        name='source',
        description='回答的網址出處'
    )
]

outputparser = StructuredOutputParser(response_schemas=response_schemas)

instructions = outputparser.get_format_instructions()
print(f'instructions: {instructions}')


prompt_tpl = PromptTemplate.from_template(
    template='請回答使用者問題.\n{input}\n{instructions}',
    partial_variables={'instructions': instructions}
)

prompt = prompt_tpl.format(input='中國有多少民族')
print('✅prompt: ',prompt)

llm = OpenAI(api_key=api_key,max_tokens=150,model_name='gpt-3.5-turbo-instruct')
output = llm.invoke(prompt)
print(f'🧭output: {output}, 🧭type: {type(output)}')

output_format = outputparser.parse(output)
print(f'🧩output_format: ')
for k, v in output_format.items():
    print(k, v)