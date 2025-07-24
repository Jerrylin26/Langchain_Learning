import re

from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import BaseOutputParser

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class UMLOutputParser(BaseOutputParser):
    @property
    def _type(self) -> str:
        return 'uml'
    
    def parse(self, text: str) :
        match = re.search(r"```(uml)?(.*)```", text, re.DOTALL)
        uml_str = match.group(2).strip()
        return uml_str
    
    def get_format_instructions(self):
        return (
            'The output should be a markdown code snippet '
            'formatted in the following schema, '
            'including the leading and trailing "```uml" and "```":\n'
            '```uml\n'
            '@startuml\n'
            '......\n'
            '@enduml\n'
            '```'
        )


output_parser = UMLOutputParser()
instructions = output_parser.get_format_instructions()

prompt_tpl = PromptTemplate.from_template(
    template='請畫一張{content}\n{instructions}',
    partial_variables={'instructions':instructions}
)

prompt = prompt_tpl.format(content='langchain應用完整開發流程圖')

llm = OpenAI(api_key=api_key, max_tokens=500, model='gpt-3.5-turbo-instruct')
output = llm.invoke(prompt)

output_format = output_parser.parse(output)
print(output_format)
