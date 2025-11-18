from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
self.index.add(embeddings.astype("float32"))


class EmbeddingManager:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = None
        self.chunks = []
    def build_faiss(self, chunks):
        self.chunks = chunks
        embeddings = self.model.encode(chunks)
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype("float32"))

    def search(self, query, top_k=3):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"), top_k
        )
        results = [self.chunks[i] for i in indices[0]]
        return results
