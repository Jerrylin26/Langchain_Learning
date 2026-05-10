from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from dotenv import load_dotenv
import os

# 載入 config
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
database=os.getenv("DB_NAME")
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
host=os.getenv("DB_HOST")
port=os.getenv("DB_PORT")

# connect SQL
# dimension: 1536
embeddings_model = OpenAIEmbeddings(api_key=api_key)
connection = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"

# data
texts = [
    "Employee name is Alex Chen. He works in engineering department.",
    "Employee name is Ryan Lin. He works in finance department.",
    "Jimmy likes basketball and supports the Warriors.",
    "Sarah works in marketing and loves traveling.",
    "The company annual meeting is held in December.",
    "Alex's manager is David.",
    "Ryan graduated from NTU.",
    "Engineering department uses Python and PostgreSQL."
]

metadatas = [{"source": "demo1"} for _ in texts]


# 儲存資料 (存進DB)
# (Postgresql)
#  add_texts: 使用我的 DB schema  from_texts: 幫我建schema
# db = PGVector.from_texts(
#     texts=texts,
#     metadatas=metadatas,
#     embedding=embeddings_model,
#     connection=connection,
#     collection_name="pgvector_chunks4" # 此為同一個vector space
# )


# 只讀已存資料
db = PGVector(
    embeddings=embeddings_model,
    connection=connection,
    collection_name="pgvector_chunks4" # 此為同一個vector space
)

''' 提升準確率流程

User Query
   ↓
Embedding
   ↓
Hybrid Search (vector + BM25) * BM25: 純 keyword-based ranking（關鍵字匹配 + 統計權重）
   ↓
metadata boost(filter) : 使用Jsonb + 自行加權，不同類別
   ↓
Top 20 chunks
   ↓
Reranker
   ↓
Top 3 chunks
   ↓
LLM answer
'''

""" Hybrid Search & metadata boost
| 方法             | 本質               | 解決什麼問題 | 缺點     |
| -------------- | ---------------- | ------ | ------ |
| BM25           | keyword matching | 精準字詞   | 不懂語意   |
| Vector         | semantic search  | 語意理解   | 可能跑偏   |
| Metadata boost | business rule    | 控制排序偏好 | 不會理解內容 |

"""

# 1. 
# 直接連DB 做SQL
docs = db.similarity_search(
    query="what is his name?",
    k=5,
    filter={"source": "demo2"}
)
for doc in docs:
    print(doc.page_content)



# 2.
# 提取搜尋資料
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 6,
        "filter": {"source": "demo"}
    }
)
# 相關性搜尋
query = 'what is his name?'
docs = retriever.invoke(query)
for doc in docs:
    print(doc.page_content)

# 等價
"""

SELECT content
FROM documents
ORDER BY embedding <-> $1
LIMIT 6;

"""

