import logging
from langchain_openai import OpenAI
from langchain.retrievers.multi_query import DEFAULT_QUERY_PROMPT
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import MultiQueryRetriever
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

embeddings_model = OpenAIEmbeddings(api_key=api_key)

# 載入網頁資料
loader = WebBaseLoader('https://blog.langchain.com/introducing-langserve/')
data = loader.load()

# 分割資料
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap=0
)
splits = splitter.split_documents(data)

# 存入向量資料
vectordb = Chroma.from_documents(splits,embeddings_model)

# 改成6個問題
prompt_tpl = PromptTemplate(
    input_variables=['question'],
    template="""You are an AI language model assistant. Your task is
    to generate 6 different versions of the given user
    question to retrieve relevant documents from a vector  database.
    By generating multiple perspectives on the user question,
    your goal is to help the user overcome some of the limitations
    of distance-based similarity search. Provide these alternative
    questions separated by newlines. Original question: {question}"""
)

# 初始化 MultiQueryRetriever
llm = OpenAI(api_key=api_key)
retriever_from_llm = MultiQueryRetriever.from_llm(vectordb.as_retriever(),llm,prompt_tpl)


# 設置日誌等級
logging.basicConfig()
logging.getLogger(
    'langchain.retrievers.multi_query'
).setLevel(logging.INFO)


# 相關性檢索
docs = retriever_from_llm.invoke('Why use LangServe?')

# 這個生成的範本
print(DEFAULT_QUERY_PROMPT.model_dump()['template'])

