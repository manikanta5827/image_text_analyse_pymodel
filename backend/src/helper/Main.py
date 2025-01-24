import asyncio
import json
import logging
import re
from helper.textExtractor import extract_text_from_image
from helper.aiProcessor import process_with_gen_ai
from helper.aiPrompt import generate_prompt

def is_json(data):
    try:
        json.loads(data)
        return True
    except (ValueError, TypeError):
        return False

def sanitize_json_string(data):
    """Sanitize the JSON string by removing or escaping invalid control characters."""
    # Remove any non-printable characters that are not escaped
    return re.sub(r'[\x00-\x1F\x7F]+', '', data)

async def extract_texts_from_images(image_paths):
    try:
        # Directly call the async function in gather
        tasks = [extract_text_from_image(path) for path in image_paths]
        texts = await asyncio.gather(*tasks, return_exceptions=True)

        return [
            text if not isinstance(text, Exception) else f"Error extracting from {image_paths[i]}"
            for i, text in enumerate(texts)
        ]
    except Exception as e:
        logging.error(f"Error extracting texts: {e}", exc_info=True)
        return []

async def process_images(image_paths, include_details=False):
    try:
        texts = await extract_texts_from_images(image_paths)
        combined_text = "\n".join(texts)
        prompt = generate_prompt(combined_text, include_details)
        structured_data = process_with_gen_ai(prompt)

        # Handle AI response
        if isinstance(structured_data, str):
            # Clean up the structured data before parsing as JSON
            structured_data = structured_data.replace("```json", "").replace("```", "")
            sanitized_data = sanitize_json_string(structured_data)
            if not is_json(sanitized_data):
                sanitized_data += '""'  
            return json.loads(sanitized_data)
        elif isinstance(structured_data, dict):
            return structured_data
        else:
            raise ValueError("Unexpected AI response format")

    except Exception as e:
        logging.error(f"Error processing images: {e}", exc_info=True)
        return {"error": "Critical error processing images"}
