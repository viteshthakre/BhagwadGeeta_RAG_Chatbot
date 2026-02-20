from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# FastAPI Backend URL
FASTAPI_URL = "http://127.0.0.1:8000/chat"

# ==========================
# HOME PAGE
# ==========================
@app.route("/")
def home():
    return render_template("chat.html")

# ==========================
# CHAT API
# ==========================
@app.route("/ask", methods=["POST"])
def ask():

    user_message = request.json["message"]

    response = requests.post(
        FASTAPI_URL,
        json={"message": user_message}
    )

    data = response.json()

    # Exact Verse Response
    if "chapter" in data:
        reply = f"""
        <div class="verse">
        <p><b> Chapter:</b> {data['chapter']}</p>
        <p><b> Verse:</b> {data['verse']}</p>

        <p><b>🕉 Shloka:</b><br>{data['shloka']}</p>

        <p><b> Transliteration:</b><br>{data['transliteration']}</p>

        <p><b> Hindi Meaning:</b><br>{data['hindi']}</p>

        <p><b> English Meaning:</b><br>{data['english']}</p>
        </div>
        """
    else:

        raw_answer = data.get("answer","Not available")

        formatted = raw_answer
        formatted = formatted.replace("Chapter:", "<p><b>Chapter:</b>")
        formatted = formatted.replace("Verse:", "</p><p><b>Verse:</b>")
        formatted = formatted.replace("Shloka:", "</p><p><b>Shloka:</b><br>")
        formatted = formatted.replace("Transliteration:", "</p><p><b>Transliteration:</b><br>")
        formatted = formatted.replace("Hindi Meaning:", "</p><p><b>Hindi Meaning:</b><br>")
        formatted = formatted.replace("English Meaning:", "</p><p><b>English Meaning:</b><br>")
        formatted = formatted.replace("Explanation:", "</p><p><b>Explanation:</b><br>")
        formatted = formatted.replace("Life Application:", "</p><p><b>Life Application:</b><br>")
        formatted = formatted.replace("Context:", "</p><p><b>Context:</b><br>")

        reply = f"""
        <div class="verse">
        {formatted}
        </p>
        </div>
        """

    return jsonify({"reply": reply})

# ==========================
# RUN APP
# ==========================
if __name__ == "__main__":
    app.run(debug=True)