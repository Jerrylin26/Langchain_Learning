from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.llm import LLMChain
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# 建立不同任務的 prompt
translation_prompt = PromptTemplate(
    template="你是一個翻譯專家，把以下文字翻譯成英文：{input}",
    input_variables=["input"]
)

math_prompt = PromptTemplate(
    template="你是一個數學助理，請計算：{input}",
    input_variables=["input"]
)

philosophy_prompt = PromptTemplate(
    template="你是一個哲學專家，請給出你對這段評論的看法：{input}",
    input_variables=["input"]
)

# LLM
llm = OpenAI(api_key=api_key)

# 子鏈
from langchain.chains import LLMChain
translation_chain = LLMChain(llm=llm, prompt=translation_prompt)
math_chain = LLMChain(llm=llm, prompt=math_prompt)
philosophy_chain = LLMChain(llm=llm, prompt=philosophy_prompt)


# Router prompt
router_str = """
- translation: 翻譯相關
- math: 數學相關
- philosophy: 哲學問題
"""

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=router_str)
# print('router_template: ',router_template)

router_prompt = PromptTemplate(template=router_template, input_variables=["input"],output_parser=RouterOutputParser())

# Router Chain
router_chain = LLMRouterChain.from_llm(llm, router_prompt)
default_chain = ConversationChain(llm=llm,output_key='text')

# MultiPromptChain 組合
# router_chain: 名字：描述 
# destination_chains: 名字: LLMChain (dict)
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains={
        "translation": translation_chain,
        "math": math_chain,
        "philosophy": philosophy_chain
    },
    default_chain=default_chain,
    verbose=True
)

# 測試
print(chain.invoke("我是一隻小小小小鳥,想要飛啊飛,卻飛也飛不高,阿阿阿! 翻譯"))
print('---------------------------------')
print(chain.invoke("5678*7777"))
print('---------------------------------')
print(chain.invoke("為政治服務的哲學還算哲學嗎?"))
print('---------------------------------')
print(chain.invoke("教我如何存第一桶金"))
