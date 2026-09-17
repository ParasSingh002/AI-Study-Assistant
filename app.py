"""
AI Study Assistant — Flask backend
-----------------------------------
Takes study notes + a question from the user, sends both to Google's
Gemini API, and returns an AI-generated answer grounded in those notes.

Flow:
1. Frontend (index.html) sends a POST request to /ask with JSON:
       { "notes": "...", "question": "..." }
2. This file builds a prompt combining the notes + question.
3. We call the Gemini API with that prompt.
4. We send the model's answer back to the frontend as JSON.
"""

import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---- Configuration ----
# Get a free Gemini API key from https://aistudio.google.com/app/apikey
# Never hardcode your real key in code you push to GitHub.
# Instead, set it as an environment variable before running:
#   export GEMINI_API_KEY="your-key-here"      (Mac/Linux)
#   set GEMINI_API_KEY=your-key-here           (Windows cmd)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)


@app.route("/")
def home():
    """Serves the main frontend page."""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """
    Receives notes + a question, asks Gemini, returns the answer.
    This is the core of the whole project.
    """
    data = request.get_json()
    notes = data.get("notes", "").strip()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    if not GEMINI_API_KEY:
        return jsonify({
            "error": "No API key configured. Set the GEMINI_API_KEY "
                     "environment variable before running the server."
        }), 500

    # This is where "Retrieval-Augmented" thinking comes in, in its
    # simplest form: we just paste the notes directly into the prompt
    # so the model answers using YOUR notes, not just general knowledge.
    if notes:
        prompt = (
            "You are a helpful study assistant. Use the notes below to "
            "answer the student's question. If the answer isn't in the "
            "notes, say so, then answer using your general knowledge.\n\n"
            f"NOTES:\n{notes}\n\n"
            f"QUESTION:\n{question}"
        )
    else:
        prompt = (
            "You are a helpful study assistant. Answer this question "
            f"clearly and simply:\n\n{question}"
        )

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        # Gemini's response is nested — we pull out just the text.
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"answer": answer})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request to Gemini failed: {str(e)}"}), 500
    except (KeyError, IndexError):
        return jsonify({"error": "Unexpected response format from Gemini."}), 500


if __name__ == "__main__":
    # debug=True auto-reloads the server when you edit code — turn off
    # for anything beyond local development.
    app.run(debug=True, port=5000)
