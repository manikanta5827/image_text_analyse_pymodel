from flask import Flask, request, jsonify
from flask_cors import CORS
from helper.Main import process_images
import logging
import asyncio
import os
import json

app = Flask(__name__, static_folder=None)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

logging.basicConfig(level=logging.DEBUG)

# Base directory for the backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '../static'))
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route("/api/food-data", methods=["OPTIONS"])
def options():
    response = jsonify({})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response, 204

@app.route("/api/food-data", methods=["POST"])
async def get_food_data():
    try:
        files = request.files.getlist('images')
        include_details = request.form.get('includeDetails', 'false').lower() == 'true'

        if not files:
            return jsonify({"error": "No images provided."}), 400

        image_paths = []
        for image in files:
            image_path = os.path.join(IMAGES_DIR, image.filename)
            await asyncio.to_thread(image.save, image_path)
            image_paths.append(image_path)

        structured_data = await process_images(image_paths, include_details)

        # Save extracted data to a JSON file in the static directory
        json_file_path = os.path.join(STATIC_DIR, 'extracted_data.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(structured_data, json_file, indent=4)

        return jsonify(structured_data), 200

    except Exception as error:
        logging.error(f"Error processing food data: {error}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route("/", methods=["GET"])
def home():
    return "Welcome to FoodAI API", 200

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 4000))
    app.run()
