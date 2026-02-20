# 🕉️ Bhagavad Gita RAG Chatbot

Bhagavad Gita RAG Chatbot is an AI-powered Retrieval-Augmented Generation (RAG) system that provides authentic knowledge from the Bhagavad Gita.  
It combines semantic search with Large Language Models to generate context-based answers grounded in scripture — ensuring minimal hallucination.

---

## ✨ Key Features

- 🎯 **Accurate Verse Retrieval**  
  Instantly fetch exact verses using inputs like `2.47`

- 🔍 **Conceptual Understanding**  
  Ask questions like *What is Dharma?* or *What is Karma Yoga?*

- 🌐 **Multilingual Support**  
  Sanskrit Shloka + Transliteration + Hindi Meaning + English Meaning

---

## 🛠️ Tech Stack

### AI Components
- **LLM:** LLaMA 3.1 via Groq API  
- **Embeddings:** all-MiniLM-L6-v2 (HuggingFace)

### Backend
- FastAPI  
- LangChain  
- FAISS Vector Database  

### Frontend
- Flask  
- HTML / CSS  

### Data Processing
- Pandas  
- Excel to JSON Pipeline  

--- 

## 🔄 System Workflow

### **Scriptural AI Search Workflow**

User Query → FAISS Vector Search → Relevant Verse Retrieval → Groq LLM (Context-Aware) → Formatted Scriptural Answer

---

## 📁 Project Structure

BHAGAVAD_GEETA_RAG/
├── backend/
│   ├── data_processing/
│   │   └── excel_to_json.py
│   ├── app.py
│   └── create_vectorDB.py
├── frontend/
│   ├── static/
│   │   ├── Bhagwad_Geeta_BG.jpeg
│   │   └── style.css
│   ├── templates/
│   │   └── chat.html
│   └── app.py
├── raw_data/
│   ├── Bhagavad_Geeta.xlsx
│   └── Bhagvad_gita_rag.json
├── vectorstore/
├── venv/
├── .gitignore
└── requirments.txt
