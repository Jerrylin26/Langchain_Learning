from langchain_openai import OpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter 
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings(api_key=api_key)

# 載入網頁資料
loader = WebBaseLoader('https://zh.wikipedia.org/zh-tw/%E6%A1%82%E8%8A%B1')
data = loader.load()

# 分割資料
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap=0
)
splits = splitter.split_documents(data)

# 存入向量資料
vectordb = Chroma.from_documents(splits,embeddings_model)

retriever = vectordb.as_retriever()

llm = OpenAI(api_key=api_key)
_filter = LLMChainFilter.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=_filter,
    base_retriever=retriever
)
compression_docs = compression_retriever.invoke('桂花的食用')
for idx, doc in enumerate(compression_docs):
    print('Document',idx+1,': ',doc.page_content)

