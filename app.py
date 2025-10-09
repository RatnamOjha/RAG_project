from src.data_loader import load_all_documents
from src.embedding import EmbeddingPipeline
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

if __name__ == "__main__":
    docs = load_all_documents("data")
    print(f"Loaded {len(docs)} documents.")
    

if __name__ == "__main__":
    
    docs = load_all_documents("data")
    emb_pipe = EmbeddingPipeline()
    chunks = emb_pipe.chunk_documents(docs)
    embeddings = emb_pipe.embed_chunks(chunks)
    print("Example embedding:", embeddings[0] if len(embeddings) > 0 else None)

if __name__ == "__main__":
    rag_search = RAGSearch()
    query = "What is machine learning?"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Summary:", summary)