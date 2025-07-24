from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.schema.output_parser import OutputParserException
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



class MovieInfo(BaseModel):
    name:str = Field(description='電影名稱')
    director:str = Field(description='電影導演')


parser = PydanticOutputParser(pydantic_object=MovieInfo)
error_info = "{'name':'美麗人生', 'director':'羅伯托.貝尼尼'}"

try:
    parser.parse(error_info)

except OutputParserException as e:
    print(e)
    fix_parser = OutputFixingParser.from_llm(
        parser=parser, 
        llm=ChatOpenAI(model="gpt-3.5-turbo",max_completion_tokens=100)
    )
    print('📟', fix_parser.parse(error_info))