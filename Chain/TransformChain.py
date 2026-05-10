from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain
from langchain.chains.transform import TransformChain
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 獲取前4段內容
def transform_func(inputs):
    text = inputs['text']
    shortened_text = '\n'.join(text.split('\n')[:4])
    
    return {'output_text': shortened_text}

transform_chain = TransformChain(
    input_variables=['text'],
    output_variables=['output_text'],
    transform=transform_func
)


# 使用者總結 TransformChain 發過來的資料
template = """ Summarize this text:
{output_text}
Summary:
"""

prompt = PromptTemplate(
    input_variables=['output_text'],
    template=template
)

llm_chain = LLMChain(llm=OpenAI(api_key=api_key), prompt=prompt)

# 串聯 transform_chain、llm_chain

sequential_chain = SimpleSequentialChain(
    chains=[transform_chain, llm_chain]
)


with open(r'.\Chain\stroy.txt', encoding='utf-8') as f:
    print(sequential_chain.invoke(f.read()))



