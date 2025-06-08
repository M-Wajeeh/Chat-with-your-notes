import streamlit as st
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3.2:1b")

# Define function to query local Ollama LLM
def query_ollama(prompt):
    response = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )
    response.raise_for_status()  # raise exception if error
    return response.json()["message"]["content"]

# Streamlit UI
st.title("Chat with Your Notes")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload your notes (PDF)", type="pdf")
user_question = st.text_input("Ask a question about your notes:")

# Function to extract text from PDF
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to chunk text
def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Function to embed and store text in FAISS
def embed_chunks(chunks, model):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index, embeddings

# Main logic
if uploaded_file:
    raw_text = extract_text(uploaded_file)
    chunks = chunk_text(raw_text)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index, _ = embed_chunks(chunks, model)

    if user_question:
        # 1. Embed the question
        q_embed = model.encode([user_question])
        D, I = index.search(np.array(q_embed), k=3)
        retrieved = [chunks[i] for i in I[0]]

        # 2. Show matched chunks
        st.write("🔍 Relevant Info:")
        for i, chunk in enumerate(retrieved):
            st.markdown(f"**Chunk {i+1}:** {chunk}")

        # 3. Create prompt and query LLM
        context = "\n\n".join(retrieved)
        full_prompt = f"""Answer the question based on the following context:\n\n{context}\n\nQuestion: {user_question}"""
        response = query_ollama(full_prompt)

        # 4. Show response
        st.markdown("### 🤖 Answer from LLM:")
        st.write(response)

        # 5. Save to chat history
        st.session_state.chat_history.append({
            "question": user_question,
            "chunks": retrieved,
            "response": response
        })

    # Optional section: Download & clear history buttons
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("## 💾 Chat History")

        # Display chat history in app
        for entry in st.session_state.chat_history:
            st.markdown(f"**Q:** {entry['question']}")
            st.markdown(f"**Answer:** {entry['response']}")
            st.markdown("---")

        # Download button (as JSON)
        chat_str = json.dumps(st.session_state.chat_history, indent=2)
        st.download_button(
            label="📥 Download Chat History (JSON)",
            data=chat_str,
            file_name="chat_history.json",
            mime="application/json"
        )

        # Clear history button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.experimental_rerun()
