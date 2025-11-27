FINAL CASE STUDY WRITE UP

EXECUTIVE SUMMARY
1) Problem: UVA has hundreds of student organizations, but most first-years—and many upper-class students—struggle to find clubs that actually match their interests. Browsing long lists on HoosInvolved is overwhelming, out-of-date, and not personalized. Students want a simple way to discover communities that fit their hobbies, identities, and goals.
2) Solution: CavaLink-GPT is a chatbot UVA club-recommender. It uses a Flask API and rule-based retrieval to generate conversational, personalized club suggestions. Students describe what they enjoy (“I like dance and consulting”), and the system returns tailored matches from club data using keyword matching. Everything runs locally inside Docker for portability and reproducibility.

SYSTEM OVERVIEW
Course Concept(s): REST APIs (Flask microservice), Containerization (Docker), Frontend to Backend integration
Architecture Diagram: Include a PNG in /assets and embed it here.
Data/Models/Services: CavaLink-GPT does not use external datasets or files. All club information is stored directly in Python as a hard-coded list of dictionaries containing each club’s name, category, tags, and description. This keeps the system lightweight and easy to run in a container. Data size is approximately 20–100 entries.

HOW TO RUN
Please run locally! 

DESIGN DECISIONS
Why this concept? Alternatives considered and why not chosen.
Tradeoffs: Performance, cost, complexity, maintainability.
Security/Privacy: Secrets mgmt, input validation, PII handling.
Ops: Logs/metrics, scaling considerations, known limitations.

RESULTS AND EVALUATION


WHAT'S NEXT
- Expand the club dataset by adding more organizations and richer tags so recommendations become more accurate and comprehensive.
- Improve keyword extraction with simple NLP techniques (tokenization, stop-word removal, stemming) to better interpret user input.
- Add better scoring logic to rank clubs using weighted matches instead of simple counts.
- Improve error handling for empty inputs, unclear queries, or malformed frontend requests.
- Add a search UI with real-time suggestions (typeahead / autocomplete).
- Allow multi-step conversations so the system can ask clarification questions (“Are you looking for competitive or social dance clubs?”).
- Enable personalization by letting users “like” or “save” recommended clubs.
- Deploy to the cloud (Render, Fly.io, or GitHub Pages + backend hosting) for public demos outside of Docker.
- Create an admin dashboard for adding/editing club info through a simple interface rather than editing Python files.

LINKS 
GitHub Repo: https://github.com/dishidhak/cavalink-gpt.git
