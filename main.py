from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_ollama import OllamaLLM 
from langchain_core.messages import SystemMessage, HumanMessage 
from sentence_transformers import SentenceTransformer

import os
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

llm = OllamaLLM(
    model="llama3",
    base_url="http://localhost:11434"
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(SCRIPT_DIR, "chroma_db")
TEXT_DIR = os.path.join(SCRIPT_DIR, "text")

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def build_vector_store():
    texts = []
    for file in os.listdir(TEXT_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(TEXT_DIR, file), "r", encoding="utf-8") as f:
                chunks = chunk_text(f.read())
                texts.extend(chunks)

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR
    )
    vectordb.persist()
    return vectordb

def get_vector_store():
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model
    )

def build_prompt(question, docs):
    system_prompt = """
Jesteś asystentem HR. Odpowiadasz tylko na podstawie dokumentów.
Jeśli nie ma odpowiedzi – napisz: "Nie znalazłam informacji w dokumentach."
"""

    context = "\n\n".join([d.page_content for d in docs])

    user_prompt = f"""
Pytanie: {question}

Fragmenty dokumentów:
{context}

Odpowiedz zgodnie z zasadami.
"""

    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

def answer_question(question):
    vectordb = get_vector_store()
    docs = vectordb.similarity_search(question, k=4)

    llm = OllamaLLM(model="mistral", temperature=0.1)

    messages = build_prompt(question, docs)
    response = llm.invoke(messages)

    return response

if __name__ == "__main__":
    if not os.path.exists(CHROMA_DIR) or len(os.listdir(CHROMA_DIR)) == 0:
        print("Buduję vector store…")
        build_vector_store()

    print("Darmowy RAG HR (Ollama + Chroma). Wpisz 'exit' aby zakończyć.\n")
    while True:
        q = input("Pytanie: ")
        if q.lower() in ["exit", "quit"]:
            break
        print(answer_question(q))
