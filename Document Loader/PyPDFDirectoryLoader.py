from langchain_community.document_loaders import PyPDFDirectoryLoader

loader = PyPDFDirectoryLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/pdf'
)

count = 0

for x in loader.load():
    count += 1
    print(x.page_content)
    print('count: ', count)