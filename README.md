CavaLink-GPT
A lightweight, AI-augmented club recommender designed to help UVA students — especially first-years — discover organizations that match their interests. Powered by a deterministic matching algorithm + TinyLlama for short natural-language explanations. Fully containerized with Docker for easy reproducibility.

1. Executive Summary
Problem
UVA has 800+ student organizations, but first-years often have trouble finding clubs that genuinely match their interests. Information is scattered across CIO pages, Instagram accounts, and random flyers.
Solution
CavaLink-GPT is a simple, reliable tool that takes a short text input (e.g., “I like dance”, “I want to code”) and returns clubs that match the student’s interests.
The system uses:
Keyword → club mapping for zero hallucination
TinyLlama (via Ollama) to generate brief, human-friendly descriptions
Docker Compose to run the entire project with one command
2. System Overview
Course Concepts Used
APIs & Microservices: Flask backend + Ollama model server
Containerization: Docker + Docker Compose
Data Handling: JSON parsing and controlled prompt generation
LLM Integration: Local TinyLlama model for natural-language responses
Architecture Diagram
Add your PNG to:
/assets/architecture.png
(Visual structure: Browser → Flask API → Ollama Model → Flask API → Browser)
Data, Models & Services
Component	Description
clubs.json	Local dataset of UVA clubs, tags, descriptions
LLM	TinyLlama via Ollama (Apache 2.0 license)
Backend	Flask API with three endpoints (/, /health, /api/chat)
Frontend	Static HTML served from /frontend/index.html
Infra	Docker Compose running backend + model as two containers
3. How to Run (Local)
Using Docker (Recommended)
# Start the full stack
docker compose up --build
This launches:
Backend: http://localhost:5000
Ollama/TinyLlama model: http://localhost:11434
Health Check
curl http://localhost:5000/health
Expected:
{"status":"ok"}
Test the Club Recommender
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"i like dance"}'
4. Design Decisions
Why These Concepts?
Deterministic keyword matching ensures no hallucinations in club selection.
TinyLlama is fast, free, and local — perfect for DS 2022 scale.
Docker Compose guarantees consistent environments on every machine.
Alternatives Considered
GPT-4 API → too costly + external dependency
Embedding search systems → more complex than needed
React frontend → unnecessary for prototype phase
Tradeoffs
Simple logic = reliable but less flexible
TinyLlama is lightweight but less expressive than larger models
Manual tagging required for new clubs
Security / Privacy
No personal data stored
No external API calls
Safe for students to use locally
Ops Notes
Logs via Docker
Can scale backend + model horizontally
First model call is slower due to warm-up
5. Results & Evaluation
Example Output
Input:
I like dance
Output:
Virginia Ke Aashiq (VKA): one-sentence summary
Hoo-Raas: one-sentence summary
Performance
Responses average 600–900ms on M-series Macs
High reproducibility thanks to Docker
Validation
Tested 15+ interest categories
Verified that no out-of-scope clubs are recommended
/health endpoint used for backend verification
6. What’s Next?
Add a styled web UI (chatbox + club cards)
Move from keyword → semantic matching
Ingest live CIO data from UVA’s database
Deploy to Render/Railway/AWS with HTTPS
Add caching + faster cold-start behavior
7. Links
GitHub Repository:
(Add your repo link here)
