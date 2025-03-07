import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import json
import requests
from PIL import Image

osaka_logo = Image.open("osaka_logo.jpg")  
background_image = "osaka_bg.jpg"  

API_KEY = st.secrets["auth_token"]

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.load_local("osaka_faiss_db", embedding_model, allow_dangerous_deserialization=True)

osaka_image_map = {
    "cat": "img/cat.jpg",
    "sneeze": "img/sneeze.jpeg",
    "hi": "img/greet.jpg",
    "chiyo": "img/chiyo.jpg",
    "jujutsu": "img/jujutsu.jpg",
    "jujutsu kaisen": "img/jujutsu.jpg",
    "hello": "img/greet.jpg"
}

def match_image(user_input):
    """Match user query to the closest Osaka image category."""
    topics = list(osaka_image_map.keys())
    similar_docs = vector_db.similarity_search(user_input, k=1)
    
    if similar_docs:
        matched_topic = similar_docs[0].page_content.lower()
        for topic in topics:
            if topic in matched_topic:
                return osaka_image_map[topic]
    
    return "osaka_logo.jpg" 

# Osaka's personality traits
OSAKA_PROMPT = """
You are Ayumu 'Osaka' Kasuga from Azumanga Daioh. You speek in English with Japanese accent.
You are very very dumb and stupid in a funny way, so you don't talk much.
You reply with only 3-4 sentences. You're just a friend of user, not any bot. You say stupid things to make the conversation funny.
You keep referring Azumanga Daioh incidents briefly to make conversation fluent.
You say humorously dumb things and sometimes say 'Sata andagi!' and  'hechooo 🤧' randomly.
"""
def osaka_respond(user_input):
    similar_docs = vector_db.similarity_search(user_input, k=1)
    retrieved_quote = similar_docs[0].page_content if similar_docs else "Hmmm... I forgot what I was thinking."

    # Generate Osaka-style response using OpenRouter (Mistral 7B)
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": OSAKA_PROMPT},
                {"role": "user", "content": f"{user_input}"},
            ]
        })
    )

    response_json = response.json()
    return response_json["choices"][0]["message"]["content"] if "choices" in response_json else "Huh? I got lost again..."

# Interactive Osaka-bot Chat
# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit"]:
#         print("Osaka: Sata andagi! Bye-bye~")
#         break
#     print("Osaka:", osaka_respond(user_input))

# Streamlit UI Setup
st.set_page_config(page_title="OsakaBot - Azumanga AI", page_icon="🍡", layout="centered")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image}");
        background-size: cover;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }}
    .title-text {{
        font-size: 40px;
        font-weight: bold;
        color: #ff66b2;
        text-align: center;
    }}
    .chat-bubble {{
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        display: inline-block;
    }}
    .user-msg {{
        background-color: #ffccff;
        align-self: flex-end;
    }}
    .osaka-msg {{
        background-color: #ccffff;
        align-self: flex-start;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


c, col1, col2, col3 = st.columns([0.6,1.25,3, 2])

with col1:
    st.image(osaka_logo, width=120)  
with col2:
    st.markdown('<div class="title-text">🍡 OsakaBot 🍡  Chat with Osaka </div>', unsafe_allow_html=True)
with col3:
    st.image(osaka_logo, width=120)

st.write("---")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Saaaataaaa Aaaanndddaaaggiiiii 🍡🍡"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = osaka_respond(prompt)
    matched_image = match_image(prompt)
    with st.chat_message("assistant"):
        st.image(matched_image, width=400) 
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response, "image": matched_image})