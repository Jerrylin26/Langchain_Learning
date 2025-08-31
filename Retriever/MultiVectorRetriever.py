from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.retrievers.multi_vector import MultiVectorRetriever
import uuid
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings(api_key=api_key)

# 載入網頁資料
loader = WebBaseLoader('https://www.nownews.com/news/6725227')
data = loader.load()

# 分割器
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
docs = text_splitter.split_documents(data)

# 批次生成摘要
summary_tpl = ChatPromptTemplate.from_template('Summarize the following document:\n\n{doc}')

chain = (
    {'doc': lambda x: x.page_content}
    | summary_tpl
    | ChatOpenAI(api_key=api_key)
    | StrOutputParser()
)
summaries = chain.batch(docs)




# 摘要向量儲存
vectorstore = Chroma(collection_name='summaries',embedding_function=embeddings_model)

# 文件存放區
store = InMemoryStore()


id_key = 'doc_id'
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key
)

# 批次生成文件對應ID
doc_ids = [str(uuid.uuid4())for _ in docs]

# 建立有摘要和文件ID的Document串列
summary_docs = [
    Document(page_content=s, metadata={id_key: doc_ids[i]}) for i,s in enumerate(summaries)
]

# 將摘要Document串列存入向量儲存
retriever.vectorstore.add_documents(summary_docs)
# 將文字區塊和對應的ID存入本機存放區
retriever.docstore.mset(list(zip(doc_ids, docs)))



# 檢索
print('--------------------docs--------------------')
retriever_docs = retriever.invoke('lulu 相關')
print(retriever_docs)

#小區塊檢索
print('--------------------sub_docs--------------------')
sub_docs = vectorstore.similarity_search('lulu 相關')
print(sub_docs)

