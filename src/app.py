import os
import json
import requests
from flask import Flask, request, jsonify, send_from_directory

# -----------------------------------------------------
# PATH SETUP
# -----------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__)

# -----------------------------------------------------
# FRONTEND ROUTES
# -----------------------------------------------------
@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/frontend/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)


# -----------------------------------------------------
# OLLAMA CONFIG
# -----------------------------------------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")

# -----------------------------------------------------
# LOAD CLUB DATA
# -----------------------------------------------------
with open(os.path.join(BASE_DIR, "assets/clubs.json"), "r") as f:
    CLUBS = json.load(f)


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200



# =====================================================
# MAIN CHAT ENDPOINT
# =====================================================
@app.post("/api/chat")
def chat():
    user_text = request.json.get("text", "").lower()
    user_words = user_text.split()

    # -------------------------------------------------
    # 1. FILTER CLUBS BY KEYWORDS
    # -------------------------------------------------
    matched = []
    for club in CLUBS:
        score = 0

        for word in user_words:
            if any(word in tag.lower() for tag in club["tags"]):
                score += 3
            if word in club["description"].lower():
                score += 2
            if word in club["name"].lower():
                score += 1

        if score > 0:
            matched.append((score, club))

    matched.sort(reverse=True, key=lambda x: x[0])
    filtered_clubs = [club for score, club in matched][:3]

    if not filtered_clubs:
        filtered_clubs = CLUBS[:2]


    # -------------------------------------------------
    # 2. SYSTEM PROMPT (STRICT RULES)
    # -------------------------------------------------
    system_prompt = """
You are CavaLink-GPT, an assistant that recommends UVA clubs.

RULES:
1. ONLY choose from the clubs listed below—never invent clubs.
2. Recommend the top 2–3 clubs that best match the user’s interests.
3. Keep explanations short (1–2 sentences).
4. Output format (exactly):

Club Name: Short explanation.
Club Name: Short explanation.
"""

    # -------------------------------------------------
    # 3. FULL PROMPT SENT TO TINYLLAMA
    # -------------------------------------------------
    full_prompt = f"""
{system_prompt}

User interests: "{user_text}"

Available clubs you may choose from:
{json.dumps(filtered_clubs, indent=2)}

Now follow the RULES and produce clean recommendations.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    # -------------------------------------------------
    # 4. CALL TINYLLAMA
    # -------------------------------------------------
    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
        data = response.json()
        reply_text = data.get("response", "").strip()

        return jsonify({
            "reply": reply_text,
            "filtered_clubs_used": filtered_clubs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# -----------------------------------------------------
# RUN FLASK
# -----------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

