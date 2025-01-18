import json
from helper.TextExtractor import extract_text_from_image
from helper.AIProcessor import process_with_gen_ai
from helper.Prompt import generate_prompt


async def process_image(image_path, include_details=False):
    try:
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)
        
        # Generate the AI prompt dynamically
        prompt = generate_prompt(extracted_text, include_details)
        
        # Process with AI asynchronously
        structured_data = await process_with_gen_ai(prompt)
        
        # Clean and parse the response
        json_response = json.loads(
            structured_data.replace("```json", "").replace("```", "").strip()
        )
        
        # Calculate and update the number of items
        json_response['No.of.items'] = len(json_response['items'])
        
        return json_response
        
    except Exception as error:
        print("Error in Main:", error)
        return {"error": "Error processing the image"}
