from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser, RetryWithErrorOutputParser
from langchain.schema.output_parser import OutputParserException
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



class Action(BaseModel):
    action:str = Field(description='要執行的動作')
    action_input:str = Field(description='動作的輸入')


parser = PydanticOutputParser(pydantic_object=Action)
prompt = PromptTemplate(
    template='請回答使用者的問題\n{instructions}\n{query}',
    input_variables=['query'],
    partial_variables={
        'instructions':parser.get_format_instructions()
    }
)

prompt_value = prompt.format_prompt(query='青花瓷的歌手是誰')
# 內容不完全,少一欄位
bad_response = '{"action":"search"}'



try:
    parser.parse(bad_response)

except OutputParserException as e:
    print(e)
    retry_parser = RetryWithErrorOutputParser.from_llm(
        parser=parser, 
        llm=ChatOpenAI(model="gpt-3.5-turbo",max_completion_tokens=100)
    )
    print('📟', retry_parser.parse_with_prompt(bad_response, prompt_value))