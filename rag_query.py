# ==========================================
# rag_query.py  (UPDATED VERSION)
# ==========================================
import os
import json
import numpy as np
import faiss
from openai import OpenAI
import httpx

# -----------------------------------------
# Paths (Auto-detected)
# -----------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "rag_index.faiss")
DATASET_PATH = os.path.join(BASE_DIR, "rag_dataset.json")

# -----------------------------------------
# OpenAI Client
# -----------------------------------------
API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(
    api_key=API_KEY,
    http_client=httpx.Client(verify=False)  # SSL workaround (dev only)
)

# -----------------------------------------
# Load FAISS Index
# -----------------------------------------
if not os.path.exists(INDEX_PATH):
    raise FileNotFoundError(f"Missing FAISS index: {INDEX_PATH}")

index = faiss.read_index(INDEX_PATH)

# -----------------------------------------
# Load Dataset
# -----------------------------------------
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Missing dataset: {DATASET_PATH}")

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

documents = data.get("documents", [])

# -----------------------------------------
# Embedding Function
# -----------------------------------------
def embed_text(text: str):
    """
    Generate embedding vector for query or prompt
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding, dtype="float32")

# -----------------------------------------
# FAISS Search
# -----------------------------------------
def faiss_search(query: str, k: int = 5):
    """
    Retrieve top-k relevant documents from FAISS
    """
    vector = embed_text(query).reshape(1, -1)
    distances, indices = index.search(vector, k)

    results = []
    for idx in indices[0]:
        idx = int(idx)
        if 0 <= idx < len(documents):
            results.append(documents[idx])

    return results

# -----------------------------------------
# RAG Answer Generator (MAIN FUNCTION)
# -----------------------------------------
def search(prompt: str, k: int = 5):
    """
    RAG pipeline:
    1. Retrieve relevant nutrition documents
    2. Use them as context
    3. Ask LLM to generate explanation / chat response
    """

    retrieved_docs = faiss_search(prompt, k)

    context = "\n\n".join(retrieved_docs)

    final_prompt = f"""
You are an intelligent nutrition assistant.

Use the following knowledge to answer clearly and logically.
Focus on explaining WHY the meals are suitable for the customer.

Knowledge Base:
{context}

User Request:
{prompt}

Answer:
"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional nutrition and diet assistant."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.4
    )

    return completion.choices[0].message.content.strip()

# -----------------------------------------
# CLI Test (Optional)
# -----------------------------------------
if __name__ == "__main__":
    q = input("Ask a nutrition question: ")
    print("\n🤖 Answer:\n")
    print(search(q))
