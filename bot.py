import ollama
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import json
import requests

# Load FAISS vector DB
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.load_local("osaka_faiss_db", embedding_model, allow_dangerous_deserialization=True)


def osaka_respond(user_input):
    # Find the most Osaka-like quote
    similar_docs = vector_db.similarity_search(user_input, k=1)
    retrieved_quote = similar_docs[0].page_content

    # Generate Osaka-style response using DeepSeek R1 (or Mistral 7B)
    response = ollama.chat(model="mistral", messages=[
        {"role": "system", "content": "You are Ayumu 'Osaka' Kasuga from Azumanga Daioh. "
                                      "You are very very shy, so you don't talk more than few words."
                                      "You speak in a slow, dreamy, and slightly random manner. "
                                      "You mix some Japanese words while speaking English."
                                      "You say humorously dumb things and sometimes say 'Sata andagi!' randomly."
                                      },
        {"role": "user", "content": f"Use this quote for inspiration: {retrieved_quote}"},
    ])
    
    return response['message']['content']

# Example
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    print("Osaka-bot:", osaka_respond(user_input))
