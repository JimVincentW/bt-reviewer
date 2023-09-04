# api.py
from flask import Flask, request, jsonify, process_url


app = Flask(__name__)

@app.route('/receive-url', methods=['POST'])
def receive_url():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Call your refactored main function that processes a URL
    results = process_url(url)
    
    return jsonify(results), 200
