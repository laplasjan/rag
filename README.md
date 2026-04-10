# rag
🧠 HR RAG Assistant (Ollama + Chroma + LangChain)
This repository contains a simple, local RAG (Retrieval-Augmented Generation) pipeline built with:

Python 3.11

Ollama (local LLM inference)

ChromaDB (vector database)

LangChain (RAG orchestration)

HuggingFace sentence embeddings

The assistant is designed to answer HR‑related questions strictly based on provided documents.
If the answer is not found in the indexed text files, the assistant responds:

"Nie znalazłam informacji w dokumentach."

📌 What is RAG?
RAG (Retrieval-Augmented Generation) is a technique where an LLM does not rely only on its internal knowledge.
Instead, it retrieves relevant text fragments from an external knowledge base (vector database) and uses them to generate accurate, grounded answers.

In this project:

Text files from the text/ directory are split into chunks.

Each chunk is embedded using a HuggingFace model.

Chroma stores these embeddings.

When the user asks a question:

the system retrieves the most relevant chunks,

builds a prompt containing only those chunks,

sends the prompt to the LLM running locally via Ollama.

This ensures the model answers only based on your documents, not hallucinations.

📁 Project Structure
Kod
project/
│
├── main.py               # The script you provided
├── text/                 # Put your .txt documents here
├── chroma_db/            # Auto-generated vector store
└── README.md             # Documentation
🧩 Requirements
Python
Python 3.11 (recommended)

Python packages
Install all required dependencies:

bash
pip install langchain langchain-core langchain-chroma langchain-huggingface langchain-ollama sentence-transformers chromadb
Depending on your environment, you may also need:

bash
pip install pydantic==1.10.13
Ollama
You must install Ollama:

https://ollama.com/download

Then pull the required models:

bash
ollama pull llama3
ollama pull mistral
HuggingFace Embeddings
The script uses:

Kod
all-MiniLM-L6-v2
This model will be downloaded automatically on first run.

▶️ How to Run
Clone the repository:

bash
git clone https://github.com/yourname/yourrepo.git
cd yourrepo
Create a virtual environment (optional but recommended):

bash
python3.11 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Install dependencies:

bash
pip install -r requirements.txt
Start Ollama in the background (it usually starts automatically).

Run the script:

bash
python main.py
On first run, the script will automatically build the vector store:

Kod
Buduję vector store…
Ask questions:

Kod
Darmowy RAG HR (Ollama + Chroma). Wpisz 'exit' aby zakończyć.

Pytanie: Jakie są zasady urlopowe?
🧠 What the Script Does
1. Loads local LLM (Ollama)
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
6. Returns the grounded answer
📝 Notes
The assistant never answers outside the documents.

You can replace the model with any Ollama-supported LLM.

You can add more .txt files to the text/ folder and rebuild the vector store.

This project is fully local — no external API calls.
