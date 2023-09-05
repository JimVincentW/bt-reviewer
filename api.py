from flask import Flask, jsonify, request
from new import DocumentHandler, WebScraper
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
        
        # Call the WebScraper to process the URL and get result data
        result_data = WebScraper.process_url(url)

        # Assuming first key of result_data is the local file name (this is just an example).
        # Modify as needed based on the structure of your returned result_data.
        first_key = list(result_data.keys())[0]
        doc_url = first_key
        date = result_data[first_key].split()[-1]  # Extract date from message like "Downloaded {local_filename}"

        # If there's additional processing you want to do after WebScraper has already downloaded files:
        downloaded_file_path = DocumentHandler.download_file(doc_url, date)
        
        # Process the documents within the "Drucksachen" directory.
        results = DocumentHandler.process_documents()
        
    except Exception as e:
        logger.exception("Failed to process URL.")  # This will log the full exception traceback
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"status": "success", "data": results}), 200
