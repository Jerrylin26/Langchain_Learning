from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

embeddings_model = OpenAIEmbeddings(api_key=api_key)

texts = [
    'Hi there!',
    'OH, Hello!',
    'What is your name?',
    'My friend call me World',
    'Hello World!',
    'John',
    'Arod',
    'I am Tony',
    'I like cake',
    'He is Iris',
    'I am his dad'
]

# 儲存資料
# (Chroma 存於 Document Transformer)
db= Chroma.from_texts(
    texts,
    embeddings_model,
    persist_directory='./Document Transformer/ChromaDB/'
)

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={'k':6}
)

# 相關性搜尋
query = 'what is his name?'
docs = retriever.invoke(query)
for doc in docs:
    print(doc.page_content)


# similarity_search = 單次查詢 API。
# as_retriever = 查詢助理

