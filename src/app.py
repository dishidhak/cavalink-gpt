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
    # FILTERING LOGIC: keyword scoring
    # -------------------------------------------------
    matched = []
    for club in CLUBS:
        score = 0
        for w in user_words:
            if w in club["name"].lower():
                score += 2
            if any(w in tag.lower() for tag in club["tags"]):
                score += 3
            if w in club["description"].lower():
                score += 1

        if score > 0:
            matched.append((score, club))

    # Sort by decreasing score
    matched = sorted(matched, reverse=True, key=lambda x: x[0])

    # Keep TOP 3 best matched clubs
    filtered_clubs = [club for score, club in matched][:3]

    # Fallback if none matched
    if not filtered_clubs:
        filtered_clubs = CLUBS[:3]


    # -------------------------------------------------
    # SYSTEM PROMPT — strict rules
    # -------------------------------------------------
    system_prompt = f"""
You are CavaLink-GPT, an assistant that recommends UVA clubs.

RULES:
1. You MUST only recommend clubs from the list below.
2. Recommend ONLY the top 2–3 clubs that best match the user’s interests.
3. Keep each recommendation SHORT (1–2 sentences).
4. Do NOT invent clubs. Do NOT modify their names.
5. NEVER output any club not shown below.
6. Final format (exact):
Club Name: Explanation.
Club Name: Explanation.

Here are the ONLY clubs you are allowed to choose from:
{json.dumps(filtered_clubs, indent=2)}

User interests: "{user_text}"
"""


    # -------------------------------------------------
    # CALL OLLAMA
    # -------------------------------------------------
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": system_prompt,
        "stream": False
    }

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

