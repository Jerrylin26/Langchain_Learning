from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/csv/1091231無障礙標章統計資料.csv',
    metadata_columns=['標章等級','登錄日期'],
    source_column='標章等級'
)

for x in loader.load():
    print(x.metadata)