import os
import json
import requests
from flask import Flask, request, jsonify, send_from_directory

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__)

# --------------------
# FRONTEND ROUTES
# --------------------
@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/frontend/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)


# Use localhost during local development
# (Docker will override this with environment variables later)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")

# Load UVA club dataset
with open("assets/clubs.json", "r") as f:
    CLUBS = json.load(f)

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/api/chat")
def chat():
    user_text = request.json.get("text", "").lower()

    # ---- 1. KEYWORD FILTERING ----
    matched_clubs = []

    for club in CLUBS:
        score = 0

        # match by name, tags, etc.
        ...
        # your filtering code stays the same
        ...

    matched_clubs.sort(reverse=True, key=lambda x: x[0])
    filtered_clubs = [club for score, club in matched_clubs][:5]

    if not filtered_clubs:
        filtered_clubs = CLUBS


    # ⭐⭐ PUT THE SYSTEM PROMPT RIGHT HERE ⭐⭐
    system_prompt = f"""
You recommend UVA clubs based ONLY on the list below.

STUDENT INTERESTS: "{user_text}"

CLUB OPTIONS:
{json.dumps(filtered_clubs, indent=2)}

Respond with ONLY 2–4 clubs that best match the student's interests.
Each response MUST follow this format exactly:

- Club Name: 1–2 sentence explanation.
- Club Name: explanation.

No extra text. No instructions. No steps. No commentary.
Begin now.
"""

    # ---- OLLAMA CALL ----
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

