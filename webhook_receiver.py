from flask import Flask, request, jsonify, abort, Response
import hmac
import hashlib
import subprocess

app = Flask(__name__)

# Secret used to validate incoming webhook payloads
WEBHOOK_SECRET = "This_1s_s0_hard"

# Endpoint to receive webhook payloads
@app.route('/webhook', methods=['POST'])
def webhook():
    # Verify webhook signature if secret is configured
    if WEBHOOK_SECRET:
        signature = request.headers.get('X-Hub-Signature')
        if not signature:
            abort(403)

        signature_parts = signature.split('=', 1)
        if len(signature_parts) != 2:
            abort(403)

        signature_type = signature_parts[0]
        expected_signature = hmac.new(WEBHOOK_SECRET.encode(), request.data, hashlib.sha1).hexdigest()
        if not hmac.compare_digest(expected_signature, signature_parts[1]):
            abort(403)

    # Process the payload
    payload = request.get_json()
    if payload:
        subprocess.run(['git', 'pull'], check=True)
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        subprocess.Popen(['nohup', 'python', 'manage.py', 'runserver', '0.0.0.0:8000'])
        print("Received payload:", payload)
        return jsonify({"message": "Webhook received successfully"}), 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, port=4040)
