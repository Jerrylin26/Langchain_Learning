from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatMessagePromptTemplate
)
from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# SystemMessagePromptTemplate & HumanMessagePromptTemplate
messages = [
    SystemMessagePromptTemplate.from_template('你的名字是{name}'),
    HumanMessagePromptTemplate.from_template('你叫什麼名字')
]

prompt_tpl =ChatPromptTemplate(
    messages,
    input_variables=['name']
)

print('🌊', prompt_tpl)

# ChatMessagePromptTemplate
messages = [
    ChatMessagePromptTemplate.from_template('你的名字是{name},請根據自己的姓名回答問題',role='system'),
    ChatMessagePromptTemplate.from_template('你叫什麼名字',role='human')
]

prompt_tpl =ChatPromptTemplate(
    messages,
    input_variables=['name']
)

print('🌊', prompt_tpl)


# ChatPromptTemplate方法
messages = [
    ('system', '你的名字是{name}，請記住，回答時要說「我叫{name}」。'),
    ('human', '你叫什麼名字')
]

prompt_tpl =ChatPromptTemplate.from_messages(
    messages=messages,

)
print('🌊', prompt_tpl)

# .format_messages: list[BaseMessage] 
# .format: BaseMessage
prompt: list[BaseMessage] = prompt_tpl.format_messages(name='阿明')
print('🌊', prompt)

llm = ChatOpenAI(temperature=0.3, api_key=api_key,max_completion_tokens=50)
print('🤗', repr(llm.invoke(prompt)))

print('🤗', llm.invoke(prompt))

print('🧭', prompt_tpl.format_prompt(name='阿明'))
print(type(prompt_tpl.format_prompt(name='阿明')))
print('🧭', prompt_tpl.format_messages(name='阿明'))
print(type(prompt_tpl.format_messages(name='阿明')))
print('🧭', prompt_tpl.format_prompt(name='阿明').to_string())