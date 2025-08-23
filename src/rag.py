import ollama
import numpy as np
from typing import Tuple
from pathlib import Path
from sentence_transformers import SentenceTransformer
from read_file import FileProcessor



class Retriever:
    """
    Class to handle retrieval of relevant chunks from a document based on a query.
    Uses SentenceTransformer for embedding and cosine similarity for retrieval.
    
    """

    def __init__(self, model_name: str = None, embedder=None):

        self.model_name = model_name if model_name else "phi4:14b"
        self.embedder = embedder if embedder else SentenceTransformer("all-MiniLM-L6-v2")
        

    def __call__(self, file_path: Path, output_folder: Path, query: str) -> Tuple[str, str] or None:
        """
        Call method to process a file using RAG.
        This method reads the file, summarizes it, saves the summary as a .txt file,
        and returns a tuple of (filename, summary).

        """
        try:
            file = FileProcessor(file_path)
            print(f"File {file_path.name} read successfully with {len(file()[1])} chunks.")
        except Exception as e:
            print(f"Error reading {file_path.name}: {e}")
            return None

        try:
            answer = self.rag_summarize(query, file()[1], file()[2])
            output_file = output_folder / f"{file_path.stem}_rag_answer.txt"
            output_file.write_text(answer, encoding="utf-8")
            print(f"RAG answer for {file_path.name} saved to {output_file}")
            return file_path.name, answer
        except Exception as e:
            print(f"Error summarizing {file_path.name}: {e}")
            return None


    def retrieve_relevant_chunks(self, query: str, chunks: list, chunk_embeddings: np.ndarray,
                                top_k: int = 3) -> list:
        """
        Retrieve top_k chunks that are most similar to the query.

        """
        query_embedding = self.embedder.encode(query)
        norms = np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
        similarities = np.dot(chunk_embeddings, query_embedding) / (norms + 1e-10)
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [chunks[i] for i in top_indices]


    def rag_summarize(self, query: str, chunks: list, chunk_embeddings: np.ndarray) -> str:

        """
        Given a document and a query, retrieve top relevant chunks and use them to prompt the LLM.
        
        """
        relevant_chunks = self.retrieve_relevant_chunks(query, chunks, chunk_embeddings, top_k=3)
        context = "\n".join(relevant_chunks)

        prompt = (f"Question: {query}\n\nContext:\n{context}\n\n"
                "Answer the question concisely based on the context:")
        response = ollama.generate(model=self.model_name, prompt=prompt)
        return response.get("response", "").strip()
    
        
        
    
        


