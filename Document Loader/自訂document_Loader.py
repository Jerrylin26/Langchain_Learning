from typing import List, Optional

from langchain.docstore.document import Document
from langchain_community.document_loaders.base import BaseLoader

class TxtLoader(BaseLoader):
    def __init__(
            self,
            filepaths: List[str],
            split_str: Optional[str] = None
    ):
    
        self.filepaths = filepaths
        self.split_str = split_str

    def load(self) -> List[Document]:

        documents = []

        for filepath in self.filepaths:
            self._generate_documents(filepath, documents)

        return documents

    def _generate_documents(self, filepath, documents):
        with open(filepath) as f:
            data = f.read().strip()

        metadata = {
            'filepath':filepath,
            'split_str':self.split_str
        }

        if self.split_str is not None:
            for split_data in data.split(self.split_str):
                documents.append(
                    Document(
                        page_content=split_data,
                        metadata = metadata
                    )
                )
        else:
            documents.append(
                Document(
                    page_content=data,
                    metadata = metadata
                )
            )


txt_loader = TxtLoader([
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/txt/羅賓.txt',
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Document Loader/txt/航海王.txt'
],split_str=',')

print(txt_loader.load())
