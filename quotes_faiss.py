import json
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

osaka_quotes = [
    "Sata andagi!",
    "I was thinkin'... but then I stopped.",
    "Penguins walk funny!",
    "Wait, what were we talking about again?",
    "If you don’t eat, you’ll get hungry.",
    "Maybe the sky is just a big blue blanket.",
    "Cows are just really big dogs, right?"
]

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_db = FAISS.from_texts(osaka_quotes, embedding=embedding_model)
vector_db.save_local("osaka_faiss_db")
print("✅ Osaka's quotes stored in FAISS!")
