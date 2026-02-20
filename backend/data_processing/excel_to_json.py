import pandas as pd
import json

# Load Excel file
file_path = r"C:\Users\91952\Videos\Bhagavad_Geeta_RAG_chatbot\raw_data\Bhagavad_Geeta.xlsx"   # <-- your file name
df = pd.read_excel(file_path)

rag_data = []

for _, row in df.iterrows():
    
    combined_text = f"""
Shloka:
{row['Shloka']}

Transliteration:
{row['Transliteration']}

Hindi Meaning:
{row['HinMeaning']}

English Meaning:
{row['EngMeaning']}

Word Meaning:
{row['WordMeaning']}
"""

    rag_format = {
        "text": combined_text.strip(),
        "metadata": {
            "id": str(row['ID']),
            "chapter": int(row['Chapter']),
            "verse": int(row['Verse'])
        }
    }

    rag_data.append(rag_format)

# Save JSON
with open(r"C:\Users\91952\Videos\Bhagavad_Geeta_RAG_chatbot\raw_data\Bhagvad_gita_rag.json", "w", encoding="utf-8") as f:
    json.dump(rag_data, f, ensure_ascii=False, indent=4)

print("✅ JSON created successfully!")
