import json
import asyncio
from TextExtractor import extract_text_from_image
from AIProcessor import process_with_gen_ai
from Prompt import generate_prompt


async def Main(image_path, include_details=False):
    try:
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)
        
        # Generate the AI prompt dynamically
        prompt = generate_prompt(extracted_text, include_details)
        
        # Process with AI
        structured_data = await process_with_gen_ai(prompt)
        
        # Clean and parse the response
        json_response = json.loads(
            structured_data.replace("```json", "").replace("```", "").strip()
        )
        
        # Calculate and update the number of items
        json_response['No.of.items'] = len(json_response['items'])
        
        # Save data to a JSON file
        with open("output.json", "w") as file:
            json.dump(json_response, file, indent=4)  # Save JSON data with formatting
            
        print("Data saved to output.json")
        
    except Exception as error:
        print("Error in Main:", error)
        return ""
        
if __name__ == "__main__":
    asyncio.run(Main('./Images/sam6.jpg'))
