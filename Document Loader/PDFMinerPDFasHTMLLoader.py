from langchain_community.document_loaders import PDFMinerPDFasHTMLLoader

loader = PDFMinerPDFasHTMLLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/pdf/kaggle競賽Image Matching Challenge 2025.pdf（副本）'
)

for idx, doc in enumerate(loader.lazy_load(), start=1):
    with open(f'page_{idx}.html', 'w', encoding='utf-8') as f:
        f.write(doc.page_content)
    print(f'✅ 已儲存 page_{idx}.html')