"""
01. AI Fluency: Core Concepts, Tokenization & Embeddings Simulator
Demonstrates foundational AI concepts including text tokenization, cosine similarity,
and basic prompt structure formatting.
"""

import math
from collections import Counter

def simple_tokenizer(text: str) -> list[str]:
    """Splits text into lowercase word tokens."""
    clean_text = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in text.lower())
    return clean_text.split()

def compute_tf_vector(tokens: list[str], vocab: list[str]) -> list[float]:
    """Computes term frequency vector for a given vocabulary."""
    counts = Counter(tokens)
    total = len(tokens) if tokens else 1
    return [counts[word] / total for word in vocab]

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Calculates cosine similarity between two numeric vectors."""
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def build_structured_prompt(role: str, task: str, constraints: list[str]) -> str:
    """Builds a structured prompt template for LLM interaction."""
    constraint_str = "\n".join(f"- {c}" for c in constraints)
    return f"System Role: {role}\n\nTask: {task}\n\nConstraints:\n{constraint_str}"

if __name__ == "__main__":
    doc1 = "Artificial intelligence and machine learning transform modern software engineering."
    doc2 = "Machine learning models and neural networks power modern artificial intelligence."
    doc3 = "Cloud computing infrastructure and database management systems."

    tokens1, tokens2, tokens3 = simple_tokenizer(doc1), simple_tokenizer(doc2), simple_tokenizer(doc3)
    vocab = sorted(list(set(tokens1 + tokens2 + tokens3)))

    v1 = compute_tf_vector(tokens1, vocab)
    v2 = compute_tf_vector(tokens2, vocab)
    v3 = compute_tf_vector(tokens3, vocab)

    print("=== AI Fluency: Semantic Similarity Demo ===")
    print(f"Similarity (Doc1 vs Doc2 - AI topics): {cosine_similarity(v1, v2):.4f}")
    print(f"Similarity (Doc1 vs Doc3 - Unrelated): {cosine_similarity(v1, v3):.4f}\n")

    prompt = build_structured_prompt(
        role="Senior Data Scientist",
        task="Explain transformer self-attention to a software engineer.",
        constraints=["Keep under 150 words", "Use a practical code analogy", "Avoid heavy math notation"]
    )
    print("=== Structured Prompt Template ===")
    print(prompt)
