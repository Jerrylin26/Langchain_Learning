from langchain_community.document_loaders import MathpixPDFLoader

loader = MathpixPDFLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/pdf/110決賽試題(含解答).pdf',
    mathpix_api_key='',
    processed_file_format='md'
)

for x in loader.load():
    print(x)