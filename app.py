from src.data_loader import load_all_documents

if __name__ == "__main__":
    docs = load_all_documents("data")
    print("Docs:", docs)
    print(f"Loaded {len(docs)} documents.")
    print("Example document:", docs[0] if docs else None)