from langchain_openai import OpenAI,ChatOpenAI
from langchain.prompts import PromptTemplate,ChatPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.chains.loading import load_chain

from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# print('---------------- OpenAI -----------------')
# print('[ 參數: llm 、prompt ]')
# llm = OpenAI(api_key=api_key)
# prompt_tpl = PromptTemplate.from_template('形容台灣的{type}')

# chain = LLMChain(llm=llm, prompt=prompt_tpl)
# print(chain.in = PromptTemplate.from_template('形容台灣的{type}')

# chain = LLMChain(llm=llm, prompt=prompt_tpl,output_key='content')
# print(chain.invoke('棒球'))


# print('-----------------------------------------')
# print('[ 輸入多個參數 ]')
# llm = OpenAI(api_key=api_key)
# prompt_tpl = PromptTemplate.from_template('形容台灣的{type},與{country}關係')

# chain = LLMChain(llm=llm, prompt=prompt_tpl)
# print(chain.invoke({'type':'棒球','country':'美國'}))



# print('-----------------------------------------')
# print('[ .apply 一筆筆跑 | .batch 批次處理 ]')
# llm = OpenAI(api_key=api_key)
# prompt_tpl = PromptTemplate.from_template('形容台灣的{type}')

# chain = LLMChain(llm=llm, prompt=prompt_tpl)
# inputs = [
#     {'type': '棒球'},
#     {'type': '美食'},
#     {'type': '演藝圈'},
# ]
# res = chain.apply(inputs)
# for info in res:
#     print(info)

# print('-----------------------------------------')
# res = chain.batch(inputs)
# for info in res:
#     print(info)


# print('-----------------------------------------')
# print('[ 結果：使用輸出解析器 ]')
# output_parser = CommaSeparatedListOutputParser()
# instructions = output_parser.get_format_instructions()

# llm = OpenAI(api_key=api_key)
# prompt_tpl = PromptTemplate.from_template('形容台灣的{type} \n{instructions}')

# chain = LLMChain(llm=llm, prompt=prompt_tpl, output_parser=output_parser)
# print(chain.invoke({'type':'棒球','instructions':instructions}))


# print('-----------------------------------------')
# print('[ 加入 verbose: 執行日誌 ]')
# llm = OpenAI(api_key=api_key)
# prompt_tpl = PromptTemplate.from_template('形容台灣的{type}')

# chain = LLMChain(llm=llm, prompt=prompt_tpl,verbose=True)
# print(chain.invoke('棒球'))
# voke('美食'))


# print('-----------------------------------------')
# print('[ 回傳值： dict ]')
# llm = OpenAI(api_key=api_key)
# prompt_tpl

print()
print('---------------- ChatOpenAI -----------------')
print('[ 參數: llm 、prompt ]')
llm = ChatOpenAI(api_key=api_key)
prompt_tpl = ChatPromptTemplate.from_messages(messages=[('human','何謂{type}')])

chain = LLMChain(llm=llm, prompt=prompt_tpl)
print(chain.invoke('女權'))


print('-----------------------------------------')
print('[ .save | .load_chain: 儲存本地匯入 ]')
llm = OpenAI(api_key=api_key)
prompt_tpl = PromptTemplate.from_template('{type}與AI應用')

chain = LLMChain(llm=llm, prompt=prompt_tpl,output_key='content')
print(chain.invoke('心理學'))

with open("./Chain/chain.json", 'w') as f:
    f.write(prompt_tpl.template)

print('-----------------------------------------')
with open("./Chain/chain.json", 'r') as f:
    load_template = f.read()

prompt_tpl = PromptTemplate.from_template(load_template)
chain = LLMChain(llm=llm, prompt=prompt_tpl,output_key='content')
print(chain.invoke('社會學'))