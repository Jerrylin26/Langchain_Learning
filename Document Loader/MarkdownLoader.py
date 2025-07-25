from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/README.md',
    mode = 'single'

)

for x in loader.load():
    print(x.metadata)