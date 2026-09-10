from app.rag import RAGRetriever


def main():

    print("Loading knowledge base...")

    rag = RAGRetriever()

    documents = rag.load_documents()

    print(
        f"Loaded {len(documents)} document chunks."
    )

    rag.build_index()

    print("FAISS index created successfully.")


if __name__ == "__main__":
    main()