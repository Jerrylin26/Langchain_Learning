from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
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
    'Hello World!'
]

# 儲存資料
db = FAISS.from_texts(texts,embeddings_model) # 預設存在RAM


# 相關性搜尋
query = 'what is his name?'
docs = db.similarity_search(query,k=2)
for doc in docs:
    print(doc.page_content)

# 儲存資料
db.save_local('./Document Transformer/FAISSDB/faiss_data')

# 載入資料
# allow_dangerous_deserialization=True 保護手續 確保load的pickle沒問題
new_db = FAISS.load_local('./Document Transformer/FAISSDB/faiss_data',embeddings_model,allow_dangerous_deserialization=True)




