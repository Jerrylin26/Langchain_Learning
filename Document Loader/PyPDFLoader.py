from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers import TesseractBlobParser

loader = PyPDFLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/pdf/創意產品設計系介紹.pdf',
    #extract_images=True,
    images_inner_format='html-img',
    images_parser=TesseractBlobParser(),
)


for x in loader.lazy_load():
    print('1:')
    print(x)

