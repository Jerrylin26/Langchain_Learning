from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from langchain.retrievers.multi_vector import MultiVectorRetriever
import uuid
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings(api_key=api_key)

# 載入網頁資料
loader = WebBaseLoader('https://www.storymami.com/story/%E4%BE%86%E8%87%AA%E5%A4%A9%E4%B8%8A%E7%9A%84%E7%8E%8B%E5%AD%90/')
data = loader.load()

# 分割器
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200)
docs = text_splitter.split_documents(data)

#function call函式描述資訊串列
functions = [
    {
        'name': 'hypothetical_questions',
        'description': 'Generate hypothetical_questions',
        'parameters':{
            'type':'object',
            'properties':{
                'questions':{
                    'type':'array',
                    'items':{'type': 'string'}
                }
            },
            'required':['questions']
        }
    }
]

# 生成假設性問題的chain
chain = (
    {'doc': lambda x: x.page_content}
    | ChatPromptTemplate.from_template(
        '生成3個假設性問題在每個doc中,並且是具有代表性的:\n\n{doc}'
    )
    | ChatOpenAI(api_key=api_key).bind(functions=functions,function_call={'name':'hypothetical_questions'})

    | JsonKeyOutputFunctionsParser(key_name='questions')
)

questions = chain.batch(docs)



# 摘要向量儲存
vectorstore = Chroma(collection_name='hypo-question',embedding_function=embeddings_model)

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
question_docs = []
for i, question_list in enumerate(questions):
    question_docs.extend(
        Document(page_content=s, metadata={id_key: doc_ids[i]}) for s in question_list)

    print(f"---------------{i}-----------------")
    


# 將摘要Document串列存入向量儲存
retriever.vectorstore.add_documents(question_docs)
# 將文字區塊和對應的ID存入本機存放區
retriever.docstore.mset(list(zip(doc_ids, docs)))



# 檢索
# 回傳 文章內容
print('--------------------docs--------------------')
retriever_docs = retriever.invoke('王子怎麼了')
print(retriever_docs)

#小區塊檢索
# 跟查詢最接近的問題
print('--------------------sub_docs--------------------')
sub_docs = vectorstore.similarity_search('王子怎麼了',k=3)
print(sub_docs)

