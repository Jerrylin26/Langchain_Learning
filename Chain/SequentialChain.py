from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

script_prompt_tpl = PromptTemplate.from_template('你是為具有潛力的心理系學生,' \
'請根據給定的領域,提出你對於結合心理學與實際可行執行層面的願景。\n領域:{field} \n 子領域:{subfield} \n 市場定位:{position}')

script_llm = OpenAI(api_key=api_key,temperature= 0.9, max_tokens=1000)

script_chain = LLMChain(llm=script_llm, prompt=script_prompt_tpl,output_key='idea')


# 建立品牌鏈
brand_prompt_tpl = PromptTemplate.from_template('你是一位接地氣創業家,對於心理學領域不了解' \
'有位心理學畢業生,想請教你關於這方面的創業概念是否可行,給出你的經驗並評價他的概念,與其他可能的子領域。\n概念:{idea}\n 目前子領域:{subfield}')

brand_llm = OpenAI(api_key=api_key,temperature= 0.5, max_tokens=600)
brand_chain = LLMChain(llm=brand_llm,prompt=brand_prompt_tpl,output_key='suggestion')

# 串起來
chain = SequentialChain(
    chains=[script_chain,brand_chain],
    verbose=True,
    input_variables=['field','subfield','position'],
    output_variables=['suggestion']
)

print(chain.invoke({'field':'商業','subfield':'AI結合心理學','position':'創新與傳統結合'}))