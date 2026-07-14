import pickle

with open("embeddings.pkl", "rb") as f:
    data = pickle.load(f)

print("\n===== TYPE OF DATA =====")
print(type(data))

print("\n===== DATA PREVIEW =====")
print(data if len(str(data)) < 2000 else str(data)[:2000])
