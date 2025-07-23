import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


class MovieInfo(BaseModel):
    name:str = Field(description='電影名稱')
    director:str = Field(description='電影導演')
    scriptwriter:str = Field(description='電影編劇')
    language:str = Field(description='電影語言')
    release_date:str = Field(description='電影上映日期')
    movie_type:str =Field(description='電影類型')
    rating:float = Field(description='電影評分')
    length:str = Field(description='電影片長')


def get_movie_html(url):
    response = requests.get(url,headers={
        'User-Agent':(
            'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/137.0.0.0 '
            'Safari/537.36'
            )
        }
    )

    html_markup = ''
    
    if response.status_code == 200:
        html_markup = response.text
        soup = BeautifulSoup(html_markup, 'html.parser')
        html_markup = str(soup.h1)

        element = soup.find(id='info')
        html_markup += str(element)

        element = soup.find(id='interest_sectl')
        html_markup += str(element)

    return html_markup




def chatgpt_parse(html):
    parser = PydanticOutputParser(pydantic_object=MovieInfo)

    messages = [HumanMessagePromptTemplate.from_template(
        template=('從以下HTML中取出電影資訊:\n{html}\n{format_instructions}')
    )]

    prompt_tpl = ChatPromptTemplate(messages=messages).format_prompt(
        html=html,
        format_instructions=parser.get_format_instructions()
    )

    llm = ChatOpenAI(api_key=api_key,max_completion_tokens=150,model_name='gpt-3.5-turbo')
    output = llm.invoke(prompt_tpl.to_messages())
    recipe = parser.parse(output.content)
    return recipe



html = get_movie_html('https://movie.douban.com/subject/36448279/')

data = chatgpt_parse(html)

print(data)
    
for k, v in data.model_dump().items():
    print(k,":", v)
