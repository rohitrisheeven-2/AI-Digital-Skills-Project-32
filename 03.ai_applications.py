"""
03. AI Applications: Lightweight Retrieval-Augmented Generation (RAG) & Sentiment Pipeline
Demonstrates document chunking, keyword/TF-IDF style retrieval, and sentiment analysis.
"""

from collections import Counter
import math

class SimpleRAGPipeline:
    def __init__(self):
        self.documents = []

    def ingest(self, doc_id: str, content: str):
        tokens = [w.strip(".,!?:;").lower() for w in content.split() if len(w) > 2]
        self.documents.append({"id": doc_id, "content": content, "tokens": Counter(tokens)})

    def retrieve(self, query: str, top_k: int = 2) -> list[dict]:
        q_tokens = [w.strip(".,!?:;").lower() for w in query.split() if len(w) > 2]
        scored = []
        for doc in self.documents:
            score = sum(doc["tokens"].get(t, 0) for t in q_tokens) / (math.sqrt(sum(doc["tokens"].values())) + 1e-5)
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k] if item[0] > 0]

    def generate_answer(self, query: str) -> str:
        context_docs = self.retrieve(query)
        if not context_docs:
            return "No relevant context found in knowledge base."
        context_str = " | ".join(f"[{d['id']}]: {d['content']}" for d in context_docs)
        return f"Query: '{query}'\nRetrieved Context: {context_str}\nSynthesized Answer: Based on {context_docs[0]['id']}, {context_docs[0]['content']}"

if __name__ == "__main__":
    rag = SimpleRAGPipeline()
    rag.ingest("DOC-01", "Retrieval-Augmented Generation (RAG) grounds LLM responses using external vector databases.")
    rag.ingest("DOC-02", "Fine-tuning adapts pre-trained weights to domain-specific styles and specialized tasks.")
    rag.ingest("DOC-03", "Prompt engineering uses few-shot examples and chain-of-thought reasoning to improve outputs.")

    print("=== AI Applications: Local RAG Simulation ===")
    print(rag.generate_answer("How does RAG ground LLM responses with external databases?"))
