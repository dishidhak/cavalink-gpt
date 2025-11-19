import os
import json
import requests
from flask import Flask, request, jsonify, send_from_directory

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__)

# Serve UI
@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/frontend/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

# Ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")

# Load clubs
with open(os.path.join(BASE_DIR, "assets/clubs.json"), "r") as f:
    CLUBS = json.load(f)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})


# ============================================================
# NO-HALLUCINATION CLUB MATCHING
# ============================================================
KEYWORD_MAP = {
    "dance": ["Virginia Ke Aashiq (VKA)", "Hoo-Raas"],
    "korean": ["Korean Student Association (KSA)"],
    "consulting": ["SEED Consulting", "180 Degrees Consulting"],
    "coding": ["Girls Who Code (GWC)", "HooHacks"],
    "data": ["Data Science and Analytics Club (DSAC)"],
    "music": ["Virginia Belles", "Cavalier Marching Band"],
    "journalism": ["Cavalier Daily"],
    "swim": ["Club Swim at UVA"],
    "finance": ["Alternative Investment Fund (AIF)"],
    "debate": ["Jefferson Society"],
    "garba": ["Hoo-Raas"],
    "raas": ["Hoo-Raas"],
    "bollywood": ["Virginia Ke Aashiq (VKA)"]
}


@app.post("/api/chat")
def chat():
    user_text = request.json.get("text", "").lower().strip()
    words = user_text.split()

    selected = []

    # match keyword → clubs
    for w in words:
        if w in KEYWORD_MAP:
            selected = KEYWORD_MAP[w]
            break

    # fallback recommendation
    if not selected:
        selected = ["Indian Student Association (ISA)"]

    # convert names → full club dict
    club_objs = [c for c in CLUBS if c["name"] in selected]

    # ============================================================
    # MODEL PROMPT — ONLY EXPLAIN CLUBS PYTHON SELECTED
    # ============================================================
    club_list_text = "\n".join([f"- {c['name']}: {c['description']}" for c in club_objs])

    prompt = f"""
You are CavaLink-GPT.

Your job: Write VERY SHORT explanations (1 sentence) ONLY for these UVA clubs:

{club_list_text}

RULES:
- Do NOT add extra clubs.
- Do NOT modify names.
- Do NOT list anything else.
- Output format EXACTLY:

Club Name: explanation.
Club Name: explanation.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
        reply = response.json().get("response", "").strip()

        return jsonify({
            "reply": reply,
            "clubs_used": club_objs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


