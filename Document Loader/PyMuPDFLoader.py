from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/pdf/kaggle競賽Image Matching Challenge 2025.pdf（副本）'
)

for x in loader.load():
    print(x)