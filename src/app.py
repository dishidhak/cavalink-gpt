import os
import json
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

# Load clubs
with open(os.path.join(BASE_DIR, "assets/clubs.json"), "r") as f:
    CLUBS = json.load(f)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

# ===============================
# NO-LLM, NO-HALLUCINATION MATCHING
# ===============================
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

    matched = []

    # Determine matching clubs
    for w in words:
        if w in KEYWORD_MAP:
            matched = KEYWORD_MAP[w]
            break

    # Fallback if nothing matched
    if not matched:
        return jsonify({"error": "no clubs that match your description"}), 200

    # Return ONLY club names + descriptions
    output = [
        {
            "name": c["name"],
            "description": c["description"]
        }
        for c in CLUBS if c["name"] in matched
    ]

    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


