from flask import Flask, send_file
import requests
import os

app = Flask(__name__)

@app.route('/wait_for_trigger', methods=['GET'])
def wait_for_trigger():

    # Read the entire content of readings.txt
    try:
        file_path = "readings.txt"
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return {"error": "File not found"}, 404
    except FileNotFoundError:
        return {"error": "File not found"}, 404

# Run the Flask app on port 5001
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
