import json
import re
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ==========================
# PATH SETTINGS
# ==========================
JSON_PATH = r"C:\Users\91952\Videos\Bhagavad_Geeta_RAG_chatbot\raw_data\Bhagvad_gita_rag.json"
VECTORSTORE_PATH = r"C:\Users\91952\Videos\Bhagavad_Geeta_RAG_chatbot\vectorstore"

print("Loading Bhagavad Gita JSON...")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

gita_docs = []

for item in data:
   
    doc = Document(
        page_content=re.search(
            r'English Meaning:(.*?)(?=Word Meaning:)',
            item["text"],
            re.DOTALL
        ).group(1).strip(),
        
        metadata={
            "chapter": int(item["metadata"]["chapter"]),
            "verse": int(item["metadata"]["verse"]),
            "id": item["metadata"]["id"],
            "full_text": item["text"]   # store full verse here
        }
    )
    gita_docs.append(doc)

print(f"Total Verses Loaded: {len(gita_docs)}")

# ==========================
# EMBEDDINGS
# ==========================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 🚨 DO NOT SPLIT VERSES
vectorstore = FAISS.from_documents(gita_docs, embeddings)

vectorstore.save_local(VECTORSTORE_PATH)

print("\nBhagavad Gita Vector DB Created Successfully!")
