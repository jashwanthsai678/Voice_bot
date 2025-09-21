# ChatGPT VoiceBot (Python / Flask)
A simple voice-enabled chatbot web app using a Python Flask backend and the browser's Web Speech APIs for speech recognition and speech synthesis.
End users **do not** need to enter any API keys — the OpenAI API key is stored as a server environment variable.

## Features
- Speak to the bot using your microphone (Chrome/Edge support).
- Bot replies using text-to-speech and shows a transcript.
- Easy one-click deploy instructions for Replit and Render.

---
## Files
- `app.py` — Flask backend (serves frontend and `/api/chat`).
- `public/index.html` — Frontend UI + JavaScript.
- `requirements.txt` — Python dependencies.
- `Procfile` — For Render (uses gunicorn).
- `.replit` — For Replit to run `python3 app.py`.

## Environment variables
Set the following environment variable in your host:
- `OPENAI_API_KEY` — Your OpenAI API key (keep this secret).
- Optional: `OPENAI_MODEL` — Model to use (default: `gpt-3.5-turbo`).

## Run locally
1. Create a virtualenv and install requirements:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create a `.env` or set `OPENAI_API_KEY` in your shell:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
3. Run:
   ```bash
   python3 app.py
   ```
4. Open `http://localhost:5000` in Chrome or Edge.

## Deploy to Replit (quick)
1. Create a new Replit and import this repo (or upload files).
2. In Replit, open the Secrets (🔒) panel and add `OPENAI_API_KEY`.
3. The `.replit` file will run `python3 app.py`. Run the repl and click the web view URL.

## Deploy to Render (quick)
1. Create a new Web Service on Render and connect your GitHub repo.
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:app`
4. In Render's Environment tab add `OPENAI_API_KEY`.
5. Deploy — Render will provide a public URL.

## Notes & tips
- Browser-side speech recognition (Web Speech API) works best in Chrome and Edge. iOS Safari has limited support.
- Keep your OpenAI key secret; never push `.env` to public Git.
- For public demos, consider adding rate-limiting or a simple authentication layer.
