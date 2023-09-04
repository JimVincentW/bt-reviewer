from flask import Flask, jsonify, request
import api_main as main  # import your refactored main script
from new import DocumentHandler
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/receive-url', methods=['POST'])
def receive_url():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "No URL provided"}), 400
        
        # Assume `main.process_url(url)` scrapes the document's URL and returns the document URL and date.
        # This part may vary depending on how your `main.process_url(url)` is structured.
        doc_url, date = main.process_url(url)
        
        # Download the document using DocumentHandler
        downloaded_file_path = DocumentHandler.download_file(doc_url, date)
        
        # If you need to further process the document, you can call the `process_documents` method.
        # This assumes that you want to process all documents within the "Drucksachen" directory.
        results = DocumentHandler.process_documents()
        
    except Exception as e:
        logger.exception("Failed to process URL.")  # This will log the full exception traceback
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"status": "success", "data": results}), 200
