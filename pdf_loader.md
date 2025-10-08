#pdf_file loading

from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from typing import List, Any
import os

def load_all_documents (data_dir:str)->List[Any]:
    data_path = Path(data_dir).resolve()
    print(f"Data_path: {data_path}")
    documents = []

    #pdf file:
    pdf_files = list(data_path.glob('**/*.pdf'))
    print(f"Found {len(pdf_files)}PDF files: {[str(f) for f in pdf_files]}")

    for pdf_file in pdf_files:
        print(f"Loading PDF: {pdf_file}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded = loader.load()
            print(f"Loaded {len(loaded)} PDFs from {pdf_file}")
            documents.extend(loaded)

        except Exception as e:
            print(f"Failed to load PDF {pdf_file}: {e}")
    return documents


