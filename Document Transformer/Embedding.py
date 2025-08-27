from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

embeddings_model = OpenAIEmbeddings(api_key=api_key)

embeddings = embeddings_model.embed_documents(
    [
        'Hi there!',
        'OH, Hello!',
        'What is your name?',
        'My friend call me World',
        'Hello World!'
    ]
)

embedded_query = embeddings_model.embed_query(
    'What was the name mentioned in the conversation?'
)
print(embedded_query)

## 流程圖
# embed_query → 「把你的問題變成向量」

# cache → 「如果這個問題以前問過，就直接拿答案（向量）不用重算」

# 向量資料庫 → 「用這個向量去找最相似的文件」

