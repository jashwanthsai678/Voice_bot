from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from flask_cors import CORS
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder='public', static_url_path='/')
CORS(app)

# Load API key and model from .env
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

# Configure OpenAI library
openai.api_key = OPENAI_API_KEY

# Log API key status
if not OPENAI_API_KEY:
    app.logger.error("❌ OPENAI_API_KEY not set. Add it in your .env file.")
else:
    app.logger.info("✅ OPENAI_API_KEY detected.")

@app.route('/api/test', methods=['GET'])
def test_key():
    if not OPENAI_API_KEY:
        return jsonify({"error": "OPENAI_API_KEY not set."}), 400
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "user", "content": "Hello!"}]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        app.logger.error(f"OpenAI test failed: {e}")
        return jsonify({"error": "OpenAI test failed", "details": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    if not OPENAI_API_KEY:
        return jsonify({'error': 'OPENAI_API_KEY is not set on the server.'}), 400

    data = request.get_json() or {}
    messages = data.get('messages')
    if not messages:
        return jsonify({'error': 'Missing "messages" in request body.'}), 400

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 600,
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        assistant_reply = (
            result.get('choices', [{}])[0]
                  .get('message', {})
                  .get('content', '')
                  .strip()
        )
        if not assistant_reply:
            return jsonify({'error': 'No reply received from OpenAI.'}), 500

        return jsonify({"reply": assistant_reply})

    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f"HTTP error: {http_err} - {response.text}")
        return jsonify({"error": "HTTP error from OpenAI", "details": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request failed: {e}")
        return jsonify({"error": "Request to OpenAI failed", "details": str(e)}), 500

# Serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
