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
    'Hello World!'
]

# 儲存資料
db= Chroma.from_texts(texts,embeddings_model,persist_directory='./Document Transformer/ChromaDB/')

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