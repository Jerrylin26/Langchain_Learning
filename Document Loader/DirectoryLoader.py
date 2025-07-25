from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/OutputParser',
    )
for x in loader.load():
    print(x)

