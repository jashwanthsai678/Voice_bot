from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from flask_cors import CORS

app = Flask(__name__, static_folder='public', static_url_path='/')
CORS(app)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    app.logger.warning("OPENAI_API_KEY not set. Add it as an environment variable before deploying.")

MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    messages = data.get('messages')
    if not messages:
        return jsonify({'error': 'messages missing'}), 400

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 600,
        "temperature": 0.75
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        j = r.json()
        assistant_reply = j.get('choices', [{}])[0].get('message', {}).get('content', '')
        return jsonify({"reply": assistant_reply})
    except requests.exceptions.RequestException as e:
        app.logger.exception("OpenAI request failed")
        return jsonify({"error": "OpenAI request failed", "details": str(e)}), 500

# Serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
