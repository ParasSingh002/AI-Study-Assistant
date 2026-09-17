# AI Study Assistant

A simple web app: paste your notes, ask a question, get an AI-generated
answer grounded in those notes — powered by Google's Gemini API.

## How it works (read this before running it)

- `app.py` — the Python/Flask **backend**. It has one important route,
  `/ask`, which receives your notes + question, builds a prompt, sends
  it to Gemini, and returns the answer as JSON.
- `templates/index.html` — the page structure (the form you see).
- `static/style.css` — makes it look decent.
- `static/script.js` — the **frontend logic**: reads what you typed,
  sends it to `/ask` using `fetch()`, and displays the result.

The request flow is:
```
Browser (script.js) --> Flask (/ask route in app.py) --> Gemini API --> back to browser
```

## Setup (step by step)

1. **Install Python** if you don't have it (3.9+).

2. **Get a free Gemini API key**:
   Go to https://aistudio.google.com/app/apikey and create one.

3. **Install dependencies**:
   ```bash
   cd ai-study-assistant
   pip install -r requirements.txt
   ```

4. **Set your API key as an environment variable** (never paste it
   directly into app.py — that's how people accidentally leak keys on
   GitHub):
   ```bash
   # Mac/Linux
   export GEMINI_API_KEY="your-key-here"

   # Windows (cmd)
   set GEMINI_API_KEY=your-key-here
   ```

5. **Run the server**:
   ```bash
   python app.py
   ```

6. Open your browser to **http://127.0.0.1:5000**

## Things to try changing, to actually learn it (not just copy it)

- Change the prompt in `app.py` to make the assistant answer in a
  different style (e.g. "explain like I'm 12", or "answer in bullet
  points only").
- Add a "summarize my notes" button that sends a different kind of
  prompt.
- Store past questions/answers in a Python list so they show up as a
  running conversation instead of one answer at a time.
- Break `app.py` on purpose (e.g. remove the API key) and read the
  error messages it produces — that's how you learn what each part
  is actually doing.

## Deploying it (so you have a live link for your resume)

Once it works locally, you can deploy the backend on **Render** (free
tier) — you'll need to set the `GEMINI_API_KEY` environment variable
in Render's dashboard instead of your terminal.

## For your resume

Once deployed:
```
AI Study Assistant | Python (Flask), HTML/CSS/JS, Gemini API
Built a web app that answers questions grounded in user-provided study
notes using Google's Gemini API, with a Flask backend and vanilla
JS/HTML frontend. [link]
```
