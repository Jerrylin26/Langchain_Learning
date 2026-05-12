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
embeddings_model = OpenAIEmbeddings(api_key=api_key,model="text-embedding-ada-002")
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
    "Engineering department uses Python and PostgreSQL.",
    "AI 免責聲明舊版本部落格參與隱私權消費者健康隱私使用規定商標 Microsoft 2026",
    "release policy 可以拆分成basic,modem,project,platform，並用來規定給出去的code"
]

metadatas = [{"source": "demo1"} for _ in texts]


# 儲存資料 (存進DB)
# (Postgresql)
#  add_texts: 使用我的 DB schema  from_texts: 幫我建schema
db = PGVector.from_texts(
    texts=texts,
    metadatas=metadatas,
    embedding=embeddings_model,
    connection=connection,
    collection_name="pgvector_chunks4" # 此為同一個vector space
)


# 只讀已存資料
# db = PGVector(
#     embeddings=embeddings_model,
#     connection=connection,
#     collection_name="pgvector_chunks4" # 此為同一個vector space
# )





retriever = db.similarity_search_with_relevance_scores(
    query="what is release policy",
    k=8
)

for doc ,score in retriever:
    print(score, doc.page_content)

