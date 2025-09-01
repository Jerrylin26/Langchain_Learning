from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import Document
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings(api_key=api_key)

# 向量庫
vectorstore = Chroma(
    collection_name="news_articles",
    embedding_function=embeddings_model
)

"""
gpt-3.5-turbo-0125	$0.50	$1.50
"""


docs = [
    Document(page_content="COVID 疫情對經濟造成嚴重影響，全球股市下跌。", metadata={"year": 2020, "author": "Alice"}),
    Document(page_content="疫苗研發成功，世界開始逐漸解封。", metadata={"year": 2021, "author": "Bob"}),
    Document(page_content="烏克蘭戰爭爆發，引起國際局勢動盪。", metadata={"year": 2022, "author": "Charlie"}),
    Document(page_content="AI 技術突破，ChatGPT 成為熱門話題。", metadata={"year": 2023, "author": "Alice"}),
    Document(page_content="美國大選激烈，兩黨爭鋒相對。", metadata={"year": 2020, "author": "David"}),
    Document(page_content="全球能源價格上漲，通膨壓力加劇。", metadata={"year": 2022, "author": "Eva"}),
    Document(page_content="奧運會在東京舉行，雖然受到疫情影響仍成功舉辦。", metadata={"year": 2021, "author": "Frank"}),
    Document(page_content="氣候變遷議題受到更多關注，各國承諾減碳。", metadata={"year": 2023, "author": "Grace"}),
    Document(page_content="火星探測計畫傳回最新照片，人類探索太空更進一步。", metadata={"year": 2021, "author": "Helen"}),
    Document(page_content="新型電動車技術問世，推動綠能產業發展。", metadata={"year": 2022, "author": "Ian"}),
]

# 加入向量庫
vectorstore.add_documents(docs)


# 定義 metadata schema
metadata_field_info = [
    AttributeInfo(
        name="year",
        description="發佈年份",
        type="integer",
    ),
    AttributeInfo(
        name="author",
        description="文章作者",
        type="string",
    ),
]

# 文件的描述
document_content_description = "新聞文章的內文"

# LLM
llm = ChatOpenAI(api_key=api_key)

# 建立 SelfQueryRetriever
retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents=document_content_description,
    metadata_field_info=metadata_field_info,
    enable_limit=True, #讓 LLM 有權解讀 k 中的數量要求
)

# 使用者查詢
docs = retriever.invoke("請找 2020 年由 Alice 撰寫，跟 COVID 相關的文章")
print(docs)
