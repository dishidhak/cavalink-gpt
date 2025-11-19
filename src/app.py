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
# MAIN CHAT ENDPOINT — ZERO HALLUCINATIONS
# =====================================================
@app.post("/api/chat")
def chat():
    user_text = request.json.get("text", "").lower().strip()
    keywords = user_text.split()

    # -------------------------------------------------
    # 1. Deterministic Keyword → Club Mapping
    # -------------------------------------------------
    KEYWORD_MAP = {
        "dance": [
            "Virginia Ke Aashiq (VKA)",
            "Hoo-Raas"
        ],
        "consulting": [
            "SEED Consulting",
            "180 Degrees Consulting"
        ],
        "korean": [
            "Korean Student Association (KSA)"
        ],
        "culture": [
            "Indian Student Association (ISA)",
            "Korean Student Association (KSA)"
        ],
        "data": [
            "Data Science and Analytics Club (DSAC)"
        ],
        "coding": [
            "Girls Who Code (GWC)",
            "HooHacks"
        ],
        "music": [
            "Virginia Belles",
            "Cavalier Marching Band"
        ],
        "journalism": [
            "Cavalier Daily"
        ],
        "swim": [
            "Club Swim at UVA"
        ],
        # fallback synonyms
        "south": ["Virginia Ke Aashiq (VKA)", "Hoo-Raas"],
        "bollywood": ["Virginia Ke Aashiq (VKA)"],
        "garba": ["Hoo-Raas"],
        "raas": ["Hoo-Raas"],
        "finance": ["Alternative Investment Fund (AIF)"],
        "debate": ["Jefferson Society"]
    }

    # Find matching clubs
    selected_names = []

    for word in keywords:
        if word in KEYWORD_MAP:
            selected_names = KEYWORD_MAP[word]
            break

    # Fallback: choose the most general club
    if not selected_names:
        selected_names = ["Indian Student Association (ISA)"]

    # Convert names → full club objects
    selected_clubs = [c for c in CLUBS if c["name"] in selected_names]


    # -------------------------------------------------
    # 2. Build TinyLlama Prompt — ONLY Explain Clubs
    # -------------------------------------------------
    prompt = f"""
You are CavaLink-GPT.

Your ONLY job is to write SHORT explanations (1–2 sentences) for the EXACT UVA clubs listed below.

STRICT RULES:
- DO NOT invent any clubs.
- DO NOT add clubs not listed.
- DO NOT modify names.
- ONLY explain the clubs provided.

User interests: "{user_text}"

Clubs to explain:
{json.dumps(selected_clubs, indent=2)}

Output formatting (EXACTLY):
Club Name: explanation.
Club Name: explanation.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    # -------------------------------------------------
    # 3. Call TinyLlama Safely
    # -------------------------------------------------
    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
        data = response.json()
        reply_text = data.get("response", "").strip()

        return jsonify({
            "reply": reply_text,
            "clubs_used": selected_clubs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# -----------------------------------------------------
# RUN FLASK
# -----------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

