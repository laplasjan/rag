<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg" />
  <img src="https://img.shields.io/badge/Ollama-Local%20LLM-orange" />
  <img src="https://img.shields.io/badge/Chroma-Vector%20DB-green" />
  <img src="https://img.shields.io/badge/LangChain-RAG-yellow" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

# 🧠 HR RAG Assistant (Ollama + Chroma + LangChain)

A lightweight, fully local **RAG (Retrieval-Augmented Generation)** system for answering HR-related questions strictly based on your own documents.  
The assistant uses:

- **Python 3.11**
- **Ollama** for local LLM inference
- **ChromaDB** as a vector store
- **LangChain** for orchestration
- **HuggingFace sentence embeddings**

If the answer is not found in the indexed documents, the assistant responds:

> *"Nie znalazłam informacji w dokumentach."*

---

## 📌 What is RAG?

**Retrieval-Augmented Generation (RAG)** is a technique where an LLM retrieves relevant information from an external knowledge base before generating an answer.  
This ensures responses are **grounded**, **accurate**, and **based on your documents**, not hallucinations.

In this project:

1. `.txt` files from the `text/` directory are split into chunks.
2. Each chunk is embedded using a HuggingFace model.
3. Chroma stores the embeddings.
4. When a user asks a question:
   - the system retrieves the most relevant chunks,
   - builds a prompt containing only those chunks,
   - sends the prompt to the local LLM via Ollama.

---

## 📁 Project Structure
'''bash
project/
│
├── main.py               # Main RAG script
├── text/                 # Place your .txt documents here
├── chroma_db/            # Auto-generated vector store
└── README.md             # Documentation
'''



---

## 🧩 Requirements

### Python
- **Python 3.11** (recommended)

### Install dependencies

You can install everything with:

bash
pip install langchain langchain-core langchain-chroma langchain-huggingface langchain-ollama sentence-transformers chromadb

Some environments may also require:

bash
pip install pydantic==1.10.13

### Install Ollama
Download Ollama:

https://ollama.com/download

Pull the required models:

bash
ollama pull llama3
ollama pull mistral

Embedding model
The script uses:

all-MiniLM-L6-v2
It will download automatically on first run.

### How to Run
Clone the repository

bash
git clone https://github.com/laplasjan/rag.git
cd rag
(Optional) Create a virtual environment

bash
python3.11 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Install dependencies

bash
pip install -r requirements.txt
Ensure Ollama is running

It usually starts automatically.

Run the script

bash
python main.py
On first run, the vector store will be built:

Kod
Buduję vector store…
Pytanie

Kod
Darmowy RAG HR (Ollama + Chroma). Wpisz 'exit' aby zakończyć.

Pytanie: Jakie są zasady urlopowe?
🧠 What the Script Does
1. Loads a local LLM via Ollama
python
llm = OllamaLLM(model="llama3")
2. Builds a vector store from .txt files
Splits text into chunks

Embeds them

Saves them to ChromaDB

3. Performs similarity search
python
docs = vectordb.similarity_search(question, k=4)
4. Builds a system + user prompt
The system prompt enforces HR‑assistant behavior and prevents hallucinations.

5. Sends the prompt to the LLM
python
response = llm.invoke(messages)
6. Returns a grounded answer
📝 Notes
The assistant never answers outside the documents.

You can add more .txt files to the text/ folder and rebuild the vector store.

Everything runs locally — no external API calls.

You can swap the LLM model to any Ollama-supported one.

🚀 Future Improvements
Web UI (FastAPI / Streamlit)

PDF ingestion

Metadata filtering

Chat history memory

📜 License
MIT License (or your preferred license)
