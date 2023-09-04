from flask import Flask, jsonify, request
import api_main as main  # import your refactored main script

app = Flask(__name__)

@app.route('/receive-url', methods=['POST'])
def receive_url():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Call your refactored main function that processes a URL
    results = main.process_url(url)
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
