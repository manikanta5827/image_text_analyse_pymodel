from flask import Flask, request, jsonify
from helper.Main import process_image
import logging
import asyncio  # Import asyncio for async support

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# API Route (Make it async to await process_image properly)
@app.route("/api/food-data", methods=["GET"])
async def get_food_data():  # Make the route asynchronous
    image_url = request.args.get("imageUrl")
    include_details = request.args.get("includeDetails", "false").lower() == "true"

    if not image_url:
        return jsonify({"error": "Missing 'imageUrl' query parameter."}), 400

    try:
        # Await the result from the asynchronous process_image function
        structured_data = await process_image(image_url, include_details)
        return jsonify(structured_data), 200
    except Exception as error:
        logging.error(f"Error processing food data: {error}")
        return jsonify({"error": str(error)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Welcome to FoodAI API", 200


# Start the server
if __name__ == "__main__":
    PORT = 3000
    app.run(host="0.0.0.0", port=PORT, debug=True)
