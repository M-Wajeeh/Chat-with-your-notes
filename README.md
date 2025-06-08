# 🧠 Chat with Your Notes

A simple and interactive app built with Streamlit that lets you upload your own PDF notes and ask questions about them using a local LLM (via Ollama). The app finds the most relevant sections of your notes and then generates a response using your chosen model (like llama3 or mistral).

---

## Features

- Upload any PDF document
- Automatic text chunking and semantic search
- Uses SentenceTransformers + FAISS for fast retrieval
- Local LLM response powered by Ollama
- Interactive UI using Streamlit
- Downloadable chat history (optional feature)

---

## Preview

![App Preview](Interface.png) 

---

## Tech Stack

- Python 3.x
- Streamlit
- PyPDF2
- sentence-transformers
- FAISS
- Ollama (local LLM runner)

---

## Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/chat-with-your-notes.git
   cd chat-with-your-notes
# 2. Create a Virtual Environment and running streamlit app 

```python -m venv venv
```venv\Scripts\activate   # For Windows
## OR
```source venv/bin/activate   # For Mac/Linux
# 3. Install Required Packages
```pip install -r requirements.txt

 .env file
```OLLAMA_HOST=http://localhost:11434
   MODEL=llama3:8b

 Making sure Ollama is running 
```ollama run llama3:8b

 Running streamlit app
```streamlit run main.py


