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

@app.post("/api/chat")
def chat():
    user_text = request.json.get("text", "").lower().strip()
    words = user_text.split()

    matches = []

    for club in CLUBS:
        searchable_text = (
            club["name"] + " " +
            club["category"] + " " +
            " ".join(club.get("tags", [])) + " " +
            club.get("description", "")
        ).lower()

        # Check if ANY user word appears in the club's searchable text
        if any(word in searchable_text for word in words):
            matches.append(club)

    if not matches:
        return jsonify({"No clubs match your description. Please try entering another keyword."}), 200

    # Format response
    output = [
        {
            "name": club["name"],
            "description": club["description"]
        }
        for club in matches
    ]

    return jsonify(output), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


