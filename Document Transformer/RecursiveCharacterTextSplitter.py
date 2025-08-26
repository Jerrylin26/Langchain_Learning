from langchain.text_splitter import RecursiveCharacterTextSplitter

doc_str = """
全球AI需求快速成長。根據國際能源總署，到2030年，資料中心電力需求將翻倍。
美國憂思科學家聯盟指出，一個AI資料中心的用電相當於一座小城市。
麻省理工學院科學家也質疑，即使單個用戶碳排降低，全球數十億用戶的總量仍很高。
他呼籲科技公司應該揭露AI模型接收查詢的頻率。
"""

text_splitter = RecursiveCharacterTextSplitter(chunk_size=20,
                                               chunk_overlap=5)

# 預設 seperator = ["\n\n", "\n", " ", ""]

docs = text_splitter.create_documents([doc_str])

for doc in docs:
    print(doc)
    print(f"length: {len(doc.page_content)}")
    print('----------------------')

