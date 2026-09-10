import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


class RAGRetriever:

    def __init__(self, knowledge_base_path="knowledge_base"):
        self.knowledge_base_path = knowledge_base_path

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.documents = []
        self.index = None

    def load_documents(self):

        self.documents = []

        for filename in os.listdir(self.knowledge_base_path):

            if filename.endswith(".txt"):

                filepath = os.path.join(
                    self.knowledge_base_path,
                    filename
                )

                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read()

                chunks = self.chunk_text(text)

                for chunk in chunks:

                    self.documents.append({
                        "source": filename,
                        "text": chunk
                    })

        return self.documents

    def chunk_text(self, text, chunk_size=500):

        words = text.split()

        chunks = []

        for i in range(0, len(words), chunk_size):

            chunk = " ".join(
                words[i:i + chunk_size]
            )

            chunks.append(chunk)

        return chunks

    def build_index(self):

        if not self.documents:
            self.load_documents()

        texts = [
            doc["text"]
            for doc in self.documents
        ]

        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True
        )

        embeddings = embeddings.astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(embeddings)

        os.makedirs(
            "data/faiss_index",
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            "data/faiss_index/index.faiss"
        )

        with open(
            "data/faiss_index/documents.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.documents,
                file,
                ensure_ascii=False,
                indent=2
            )

    def load_index(self):

        self.index = faiss.read_index(
            "data/faiss_index/index.faiss"
        )

        with open(
            "data/faiss_index/documents.json",
            "r",
            encoding="utf-8"
        ) as file:

            self.documents = json.load(file)

    def retrieve(self, query, top_k=3):

        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            document = self.documents[index].copy()

            document["score"] = float(distance)

            results.append(document)

        return results