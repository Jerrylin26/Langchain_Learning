from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

messages=[
    SystemMessagePromptTemplate.from_template('請問不超過{num}個字來總結以下對話'),
    MessagesPlaceholder('context'),
    HumanMessagePromptTemplate.from_template(template='###請開始總結以上對話'),
]

# 大架構
prompt = ChatPromptTemplate.from_messages(messages)

human_message= HumanMessage('如何學好程式設計')
ai_message = AIMessage('學好程式設計的關鍵在於打好語法與邏輯思維基礎，理解變數、條件、迴圈、函式等核心概念，再進一步學習資料結構與演算法；透過持續實作小專案與解題練習來強化實力，同時掌握 Git、API、資料庫等實務技能。選擇一個有興趣的方向深入，如網頁、AI、App 或遊戲，搭配閱讀他人程式碼與參與社群交流，才能穩健成長為真正的開發者。')

prompt_messages = prompt.format_messages(context=[human_message, ai_message], num=50)

for message in prompt_messages:
    print('🧩', repr(message))

llm = ChatOpenAI(temperature=0.3, api_key=api_key,max_completion_tokens=50)
print('🤗', repr(llm.invoke(prompt_messages)))
