from langchain_community.document_loaders import UnstructuredPDFLoader

loader = UnstructuredPDFLoader(
    'https://arxiv.org/pdf/2507.17767'
)

for x in loader.load():
    print(x)