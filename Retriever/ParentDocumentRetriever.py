from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings(api_key=api_key)

# 載入網頁資料
loader = WebBaseLoader('https://www.nownews.com/news/6725227')
data = loader.load()

# 大小區塊分割器
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

# 存小區塊向量儲存
vectorstore = Chroma(embedding_function=embeddings_model)

# 大區塊存放區
store = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)

retriever.add_documents(data)

# 檢索
print('--------------------docs--------------------')
retriever_docs = retriever.invoke('RAG related')
print(retriever_docs)

#小區塊檢索
print('--------------------sub_docs--------------------')
sub_docs = vectorstore.similarity_search('RAG related')
print(sub_docs)

