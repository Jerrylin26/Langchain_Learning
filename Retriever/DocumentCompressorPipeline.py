from langchain_openai import OpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from langchain.retrievers.document_compressors import EmbeddingsFilter,DocumentCompressorPipeline
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings(api_key=api_key)

# 載入網頁資料
loader = WebBaseLoader('https://zh.wikipedia.org/zh-tw/%E6%A1%82%E8%8A%B1')
data = loader.load()

# 分割資料
splitter = CharacterTextSplitter(
    chunk_size = 180,
    chunk_overlap=0
)
redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings_model)
relevant_filter = EmbeddingsFilter(embeddings=embeddings_model,similarity_threshold=0.865)
pipeline_compressor = DocumentCompressorPipeline(transformers=[splitter,redundant_filter,relevant_filter])

split = splitter.split_documents(data)
# 存入向量資料
vectordb = Chroma.from_documents(split,embeddings_model)

retriever = vectordb.as_retriever()


compression_retriever = ContextualCompressionRetriever(
    base_compressor=pipeline_compressor,
    base_retriever=retriever
)
compression_docs = compression_retriever.invoke('桂花的食用')
for idx, doc in enumerate(compression_docs):
    print('Document',idx+1,': ',doc.page_content)



