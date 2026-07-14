import os
import requests
import json
import numpy as np
import faiss
import pickle
import httpx
from openai import OpenAI

# ==========================
#  OpenAI Client (SSL FIX)
# ==========================
API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(
    api_key=API_KEY,
    http_client=httpx.Client(verify=False)   # 🔥 FIX SSL ERROR
)

DATA_URL = "http://127.0.0.1:8000/rag/export/"


# ==========================
#  LOAD DJANGO DATA
# ==========================
print("📥 Fetching data from Django...")

response = requests.get(DATA_URL)
data = response.json()

documents = []

# -----------------------------
# Convert Django data to text
# -----------------------------
for rest in data["restaurants"]:
    documents.append(
        f"Restaurant: {rest['name']} located at {rest['address']} phone {rest['phone']}."
    )

for meal in data["meals"]:
    documents.append(
        f"Meal: {meal['name']}. Description: {meal['description']}. "
        f"Calories: {meal['calories']}. Protein: {meal['protein']}. "
        f"Carbs: {meal['carbs']}. Fat: {meal['fat']}."
    )

for cust in data["customers"]:
    documents.append(
        f"Customer: {cust['name']} age {cust['age']} weight {cust['weight']} "
        f"height {cust['height']} goal is {cust['goal']} likes {cust['likes']} "
        f"dislikes {cust['dislikes']} allergies {cust['allergies']}."
    )

print(f"📄 Total documents: {len(documents)}")



# ==========================
#  EMBEDDING FUNCTION
# ==========================
def embed(text):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(res.data[0].embedding, dtype="float32")



# ==========================
#  GENERATE EMBEDDINGS
# ==========================
print("🧠 Generating embeddings...")

embeddings = np.array([embed(doc) for doc in documents], dtype="float32")



# ==========================
#  BUILD FAISS INDEX
# ==========================
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "rag_index.faiss")



# ==========================
#  SAVE DATASET
# ==========================
dataset = {
    "documents": documents,
    "embeddings": embeddings.tolist()
}

with open("rag_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4)

print("✅ RAG database built successfully!")
print(f"📄 Documents: {len(documents)}")
