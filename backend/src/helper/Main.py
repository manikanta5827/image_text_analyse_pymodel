import asyncio
import logging
from helper.textExtractor import extract_text_from_image
from helper.aiProcessor import process_with_gen_ai
from helper.aiPrompt import generate_prompt
from helper.jsonParser import jsonParser

async def extract_texts_from_images(image_paths):
    try:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(None, extract_text_from_image, path) for path in image_paths]
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
        print(f'text : {combined_text}')
        prompt = generate_prompt(combined_text, include_details)
        structured_data = process_with_gen_ai(prompt)
        parsed_data = jsonParser(structured_data)
        return parsed_data   

    except Exception as e:
        logging.error(f"Error [ in Main file ] processing images: {e}", exc_info=True)
        return {"error": "Critical error processing images"}

