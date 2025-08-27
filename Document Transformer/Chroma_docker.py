from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import uuid
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

embeddings_model = OpenAIEmbeddings(api_key=api_key)

client = chromadb.HttpClient(
    '127.0.0.1',
    port = 8000,
    settings=Settings(allow_reset=True)
)

# client.reset()

# Collection
# 存放 embeddings + metadata 的「表格」

db= Chroma(client=client,collection_name='my_collection',embedding_function=embeddings_model)


texts = [
    'Hi there!',
    'OH, Hello!',
    'What is your name?',
    'My friend call me World',
    'Hello World!'
]


# 儲存資料
db.add_texts(texts=texts,ids=[str(uuid.uuid1()) for _ in range(len(texts))])



# 相關性搜尋
query = 'what is his name?'
docs = db.similarity_search(query,k=2)
for doc in docs:
    print(doc.page_content)

print('---------------------------')

docs = db.similarity_search_with_relevance_scores(query)
for doc in docs:
    print(doc)
print('---------------------------')


# MMR（最大邊際相關性） 會避免結果太相似，保證結果更「多樣化」
docs = db.max_marginal_relevance_search(query)
for doc in docs:
    print(doc.page_content)
print('---------------------------')