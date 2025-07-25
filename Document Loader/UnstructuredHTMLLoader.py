from langchain_community.document_loaders import UnstructuredHTMLLoader,BSHTMLLoader

# 抓取 並會分段text
loader = UnstructuredHTMLLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/html/exercise.html'
)

for x in loader.load():
    print(x)

print('-********************************************')

# 用BeautifulSoup 抓取全部text 較不精準
loader = BSHTMLLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/html/exercise.html',
)

for x in loader.load():
    print(x.page_content)