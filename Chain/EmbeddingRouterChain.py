from langchain.chains.router import MultiPromptChain
from langchain.chains.router.embedding_router import EmbeddingRouterChain
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.llm import LLMChain
from langchain_openai import OpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
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




names_and_descriptions = [
    ('translation',['翻譯文字','將中文轉英文']),
    ('math',['數學計算','數字運算','財務計算']),
    ('philosophy',['哲學問題','人生問題','價值觀討論'])
]
# Router Chain
router_chain = EmbeddingRouterChain.from_names_and_descriptions(
    names_and_descriptions=names_and_descriptions,
    vectorstore_cls=Chroma,
    embeddings=OpenAIEmbeddings(api_key=api_key),
    routing_keys=['input']
)
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
print(chain.invoke("我是一隻小小小小鳥,想要飛啊飛,卻飛也飛不高,阿阿阿! 要跟外國人說"))
print('---------------------------------')
print(chain.invoke("一個禮拜存3000,一年後能買多少雙Nike球鞋"))
print('---------------------------------')
print(chain.invoke("我想知道人生的意義是什麼?"))
print('---------------------------------')
print(chain.invoke("教我如何成為一名lamboghini擁有者"))
print('---------------------------------')
print(chain.invoke("我想在明年買房前，先計算存款和投資收益"))
