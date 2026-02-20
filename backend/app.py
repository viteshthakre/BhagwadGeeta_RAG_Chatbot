import os
import re
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

app = FastAPI(title="Bhagavad Gita RAG API")

# ==========================
# LOAD VECTOR DB
# ==========================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    r"C:\Users\91952\Videos\Bhagavad_Geeta_RAG_chatbot\vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

# ==========================
# LLM
# ==========================
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================
# METADATA INDEX
# ==========================
metadata_index = {}

all_docs = vectorstore.docstore._dict.values()

for doc in all_docs:
    ch = int(doc.metadata.get("chapter"))
    vs = int(doc.metadata.get("verse"))
    metadata_index[(ch, vs)] = doc

# ==========================
# REQUEST MODEL
# ==========================
class Query(BaseModel):
    message: str

# ==========================
# BOOK INFO STATIC
# ==========================
def check_book_info(question):

    q = question.lower()

    if "how many chapter" in q:
        return "📖 Bhagavad Gita has 18 Chapters."

    if "how many verse" in q:
        return "🧾 Bhagavad Gita has 700 Verses."

    if "who spoke" in q:
        return "🗣️ Lord Krishna spoke Bhagavad Gita to Arjuna."

    return None

# ==========================
# CHAPTER VERSE DETECTOR
# ==========================
def extract_chapter_verse(text):

    text = text.lower()

    patterns = [
        r'chapter\s*(\d+)\s*verse\s*(\d+)',
        r'chpt\s*(\d+)\s*verse\s*(\d+)',
        r'ch\s*(\d+)\s*v\s*(\d+)',
        r'c\s*(\d+)\s*v\s*(\d+)',
        r'(\d+)\s*:\s*(\d+)',
        r'(\d+)\s*\.\s*(\d+)',
        r'\b(\d+)\s+(\d+)\b',
        r'adhyay\s*(\d+)\s*shlok\s*(\d+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1)), int(match.group(2))

    return None, None

# ==========================
# TEXT EXTRACTOR
# ==========================
def extract_sections(text):

    shloka = re.search(r'Shloka:(.*?)(?=Transliteration:)', text, re.DOTALL)
    translit = re.search(r'Transliteration:(.*?)(?=Hindi Meaning:)', text, re.DOTALL)
    hindi = re.search(r'Hindi Meaning:(.*?)(?=English Meaning:)', text, re.DOTALL)
    english = re.search(r'English Meaning:(.*?)(?=Word Meaning:)', text, re.DOTALL)

    return (
        shloka.group(1).strip() if shloka else "N/A",
        translit.group(1).strip() if translit else "N/A",
        hindi.group(1).strip() if hindi else "N/A",
        english.group(1).strip() if english else "N/A"
    )

# ==========================
# CHAT API
# ==========================
@app.post("/chat")
def chat(query: Query):

    question = query.message

    # 1️ Book Info Check
    book_info = check_book_info(question)
    if book_info:
        return {"answer": book_info}

    # 2 Exact Verse Check
    chapter, verse = extract_chapter_verse(question)

    if chapter and verse:
        doc = metadata_index.get((chapter, verse))
        if doc:
            shloka, translit, hindi, english = extract_sections(doc.metadata["full_text"])   #extract_sections(doc.page_content)
            return {
                "chapter": chapter,
                "verse": verse,
                "shloka": shloka,
                "transliteration": translit,
                "hindi": hindi,
                "english": english
            }

    # 3 Semantic Retrieval
    docs_with_score = vectorstore.similarity_search_with_score(question, k=4)

    threshold = 1.35

    relevant_docs = [
        doc for doc, score in docs_with_score
        if score < threshold
    ]

    if not relevant_docs:
        return {"answer": "Not available in Bhagavad Gita database"}

    # context = "\n\n".join(doc.metadata["full_text"] for doc in relevant_docs)
    context = ""
    
    for i, doc in enumerate(relevant_docs):
        context += f"""
    Verse {i+1}:
    {doc.metadata["full_text"]}
    -----------------------
    """
    # 4 Prompt
    prompt = f"""
You are a Bhagavad Gita Wisdom Guide.

The user may ask:
- Philosophical questions
- Daily life problems
- Emotional struggles
- Conceptual explanations
- Comparative analysis between teachings

You will receive multiple Bhagavad Gita verses in the Context.

Your responsibilities:

1. Carefully understand the user's question or life situation.
2. From the provided Context, SELECT ONLY the most relevant verse(s)
   that directly answer the user's question.
3. DO NOT combine Sanskrit, Transliteration, or Meanings from different verses.
4. Treat each verse independently.
5. Extract EXACTLY from the selected verse(s):
   - Chapter Number
   - Verse Number
   - Sanskrit Shloka
   - Transliteration
   - Hindi Meaning
   - English Meaning
6. If the question is analytical or comparative,
   explain the relationship between the selected verses
   based ONLY on the English Meaning.
7. If the question is life-based,
   explain how the teaching applies to real-life situations.

STRICT RULES:
- Use ONLY the provided Context.
- DO NOT create your own verse or translation.
- DO NOT hallucinate Sanskrit or meanings.
- DO NOT mix different verses together.
- DO NOT use emojis or decorative symbols.
- Always provide Chapter and Verse reference.

If no verse in the Context is relevant, reply EXACTLY:
No relevant teaching found in Bhagavad Gita for this query.

Answer Format:

Chapter:
Verse:

Shloka:

Transliteration:

Hindi Meaning:

English Meaning:

Explanation:

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {"answer": response.content.strip()}

