from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_transformers import LongContextReorder
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings(api_key=api_key)

texts= [
    "釣魚需要耐心等待魚上鉤。",
    "湖邊是最適合釣魚的地方之一。",
    "許多人喜歡週末和朋友一起去釣魚。",
    "釣魚是一種放鬆身心的休閒活動。",
    "棒球是一項受歡迎的團隊運動。",
    "投手和打者的對決是比賽的精華。",
    "選擇合適的魚餌能增加釣魚成功率。",
    "清晨和黃昏通常是釣魚的好時機。",
    "全壘打總能引起觀眾的歡呼。",
    "棒球需要團隊合作和策略。"
]

retriever = Chroma.from_texts(
    texts=texts,
    embedding=embeddings_model
).as_retriever()

query = "釣魚啊走摟"

docs = retriever.invoke(query)
print('before:\n')
for doc in docs:
    print(doc)


reordering = LongContextReorder()
reordered_docs = reordering.transform_documents(docs)
print()
print('after:\n')
for doc in reordered_docs:
    print(doc)
    print()


