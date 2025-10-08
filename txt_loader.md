from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import TextLoader
import os

def load_documents(data_dir: str)->List[Any]:
    data_path = Path(data_dir).resolve()
    print(f"Data path: {data_path}")
    documents = []

    #txt files:
    txt_files = list(data_path.glob('**/*.txt'))
    print(f"Found {len(txt_files)} TXT files: {[str(f) for f in txt_files]}")
    for txt_file in txt_files:
        print(f"Loading TXT: {txt_file}")
        try:
            loader = TextLoader(str(txt_file), encoding='utf8')
            loaded = loader.load()
            print(f"Loaded {len(loaded)} TXT docs from {txt_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"Failed to load TXT {txt_file}: {e}")
    return documents
