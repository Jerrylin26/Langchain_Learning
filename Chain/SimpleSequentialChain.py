from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

script_prompt_tpl = PromptTemplate.from_template('你是為具有潛力的心理系學生,' \
'請根據給定的領域:{field},提出你對於結合心理學與實際可行執行層面的願景')

script_llm = OpenAI(api_key=api_key,temperature= 0.9, max_tokens=1000)

script_chain = LLMChain(llm=script_llm, prompt=script_prompt_tpl)


# 建立品牌鏈
brand_prompt_tpl = PromptTemplate.from_template('你是一位接地氣創業家,對於心理學領域不了解' \
'有位心理學畢業生,想請教你關於這方面的創業概念是否可行,給出你的經驗並評價他的概念。概念:{idea}')

brand_llm = OpenAI(api_key=api_key,temperature= 0.5, max_tokens=600)
brand_chain = LLMChain(llm=brand_llm,prompt=brand_prompt_tpl)

# 串起來
chain = SimpleSequentialChain(
    chains=[script_chain,brand_chain],
    verbose=True
)

print(chain.invoke('商業'))