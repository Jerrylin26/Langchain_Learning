from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings(api_key=api_key)

doc_list = [
    'I like apples',
    'I like orange',
    'Apples and oranges are fruits'
]

bm25_retriever = BM25Retriever.from_texts(doc_list)


vectorstore = Chroma.from_texts(doc_list, embeddings_model)
retriever = vectorstore.as_retriever()

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever,retriever],
    weights=[0.5,0.5]
)

docs = ensemble_retriever.invoke('apples')

for doc in docs:
    print(doc)


