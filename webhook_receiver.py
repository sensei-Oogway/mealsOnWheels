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
    python_interpreter = 'C:/Users/DrAks/PycharmProjects/pythonProject/venv/Scripts/python'
    # Process the payload 
    payload = request.get_json()
    if payload:
        subprocess.run(['git', 'pull'], check=True)
        subprocess.run([python_interpreter, 'manage.py', 'migrate'], check=True)
        subprocess.Popen([python_interpreter, 'manage.py', 'runserver'])
        print("Received payload:", payload)
        return jsonify({"message": "Webhook received successfully"}), 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, port=4444)
