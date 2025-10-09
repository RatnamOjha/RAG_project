## RAGify-Docs

Retrieval-Augmented Generation (RAG) demo that loads local documents (PDF/TXT/CSV/Excel/Word/JSON), chunks and embeds them with Sentence-Transformers, indexes with FAISS, and answers questions using context-retrieved chunks summarized by a Groq LLM.

### Features
- **Multi-format loading**: PDF, TXT, CSV, Excel, Word, JSON (recursive under `data/`).
- **Chunking**: `RecursiveCharacterTextSplitter` with configurable `chunk_size` and `chunk_overlap`.
- **Embeddings**: `sentence-transformers` (default `all-MiniLM-L6-v2`).
- **Vector store**: Local FAISS index persisted under `faiss_store/`.
- **RAG query**: Retrieve top-k chunks and summarize with Groq `ChatGroq`.

### Project Structure
```text
RAGify-Docs/
  app.py                  # Example pipeline usage (load, embed, search)
  main.py                 # Simple entry stub
  src/
    data_loader.py        # Multi-format loaders -> LangChain Documents
    embedding.py          # Chunking + embeddings pipeline
    vectorstore.py        # FAISS persistence and search
    search.py             # RAGSearch: retrieval + LLM summarization
  data/                   # Your source documents (scanned recursively)
  faiss_store/            # Persisted FAISS index + metadata
  requirements.txt        # Python deps (pip)
  pyproject.toml          # Project metadata & deps (uv/pip)
  notebook/document.ipynb # Optional experimentation
```

### Prerequisites
- Python 3.9+
- macOS/Linux/Windows

### Installation
You can use either pip (requirements.txt) or uv (pyproject).

Using pip:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Using uv (if installed):
```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
# or
uv sync
```

Key dependencies (see `pyproject.toml`): `chromadb`, `faiss-cpu`, `langchain`, `langchain-community`, `langchain-core`, `pypdf`, `pymupdf`, `sentence-transformers`.

### Environment Variables (Groq LLM)
The RAG summarization uses Groq via `langchain-groq`. Create a `.env` file in the project root with:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

Note: `src/search.py` currently sets `groq_api_key = ""`. Update it to read from the environment:
```python
# in src/search.py
import os
from dotenv import load_dotenv
load_dotenv()
...
groq_api_key = os.getenv("GROQ_API_KEY", "")
self.llm = ChatGroq(groq_api_key=groq_api_key, model_name=llm_model)
```

### Preparing Your Data
Place documents anywhere under the `data/` folder; the loader scans recursively.
Examples:
```text
data/
  pdf/
    your_doc.pdf
  text_files/
    notes.txt
  spreadsheets/
    table.xlsx
  word/
    report.docx
  json/
    knowledge.json
```
Supported extensions: `.pdf`, `.txt`, `.csv`, `.xlsx`, `.xls`, `.docx`, `.doc`, `.json`.

### How It Works (High Level)
1. `load_all_documents("data")` loads and converts files to LangChain `Document`s.
2. `EmbeddingPipeline` splits documents and generates embeddings with `SentenceTransformer`.
3. `FaissVectorStore` adds vectors, persists index/metadata to `faiss_store/`.
4. `RAGSearch` retrieves relevant chunks for a query and asks a Groq LLM to summarize.

### Quickstart
Once dependencies are installed and `GROQ_API_KEY` is set:
```bash
python app.py
```
`app.py` demonstrates:
- loading documents
- chunking + embeddings
- an example RAG search-and-summarize call

To query programmatically:
```python
from src.search import RAGSearch

rag = RAGSearch(persist_dir="faiss_store", embedding_model="all-MiniLM-L6-v2", llm_model="llama-3.1-8b-instant")
answer = rag.search_and_summarize("What is machine learning?", top_k=3)
print(answer)
```

If `faiss_store/` does not exist yet, `RAGSearch` will build it from `data/` on first run.

### CLI-like Usage Examples
- Build (implicitly happens on first query if store missing):
```bash
python -c "from src.data_loader import load_all_documents; from src.vectorstore import FaissVectorStore; docs=load_all_documents('data'); vs=FaissVectorStore(); vs.build_from_documents(docs)"
```

- Search with an ad-hoc query using the existing store:
```bash
python -c "from src.search import RAGSearch; r=RAGSearch(); print(r.search_and_summarize('Summarize neural networks', top_k=5))"
```

### API Reference
- `src/data_loader.py`
  - `load_all_documents(data_dir: str) -> List[Any]`
    - Recursively loads PDF/TXT/CSV/Excel/Word/JSON into LangChain `Document`s. Prints debug info.

- `src/embedding.py`
  - `EmbeddingPipeline(model_name: str = "all-MiniLM-L6-v2", chunk_size: int = 1000, chunk_overlap: int = 150)`
  - `chunk_documents(documents) -> List[Any]` — uses `RecursiveCharacterTextSplitter`.
  - `embed_chunks(chunks) -> np.ndarray` — encodes text with `SentenceTransformer`.

- `src/vectorstore.py`
  - `FaissVectorStore(persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", chunk_size: int = 1000, chunk_overlap: int = 150)`
  - `build_from_documents(documents)` — chunks, embeds, persists FAISS index + metadata.
  - `add_embeddings(embeddings, metadatas)` — adds vectors and optional metadata.
  - `save()` / `load()` — persist/read index and metadata.
  - `query(query_text: str, top_k: int = 5)` — returns nearest neighbors with distances + metadata.

- `src/search.py`
  - `RAGSearch(persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "llama-3.1-8b-instant")`
  - `search_and_summarize(query: str, top_k: int = 5) -> str` — retrieves top-k chunks and summarizes with Groq LLM.

### Notes and Caveats
- Ensure `GROQ_API_KEY` is configured; otherwise the LLM call will fail or produce no output.
- The initial build may take time depending on corpus size and model download.
- FAISS indices and `metadata.pkl` are written to `faiss_store/`. Delete this directory to rebuild from scratch.
- If you reorganize `data/`, rebuild the store to reflect the changes.

### Troubleshooting
- "No relevant documents found": Ensure `data/` contains supported files and the store is built.
- Import errors for loaders: Verify versions in `requirements.txt` or install via `pyproject.toml`.
- Groq auth issues: Confirm `GROQ_API_KEY` in `.env` and that `python-dotenv` is installed.

### License
Add your preferred license here.