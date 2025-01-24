import easyocr
import cv2
import asyncio
from helper.imagePreProcessor import preprocess_image 
import aiofiles
import os

# Base directory for the backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../static'))
TEMP_IMAGE_PATH = os.path.join(STATIC_DIR, 'temp_preprocessed_image.jpg')
TEXT_FILE_PATH = os.path.join(STATIC_DIR, 'extracted_data.txt')

# Ensure the static directory exists
os.makedirs(STATIC_DIR, exist_ok=True)

async def save_file_async(file_path, content, is_image=False):
    """
    Asynchronously saves content to a file.
    :param file_path: Path where the content will be saved.
    :param content: Content to save (image or text).
    :param is_image: True if the content is an image; False for text.
    """
    try:
        if is_image:
            # Save image asynchronously
            await asyncio.to_thread(cv2.imwrite, file_path, content)
            print(f"Image saved at {file_path}")
        else:
            # Save text file asynchronously
            async with aiofiles.open(file_path, mode='w') as file:
                await file.write(content)
                print(f"Text saved at {file_path}")
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")


async def extract_text_from_image(image_path):
    try:
        # Preprocess the image
        preprocessed_img = preprocess_image(image_path)
        if preprocessed_img is None:
            raise ValueError("Preprocessing failed.")

        # Convert grayscale image back to BGR for visualization
        preprocessed_img_bgr = cv2.cvtColor(preprocessed_img, cv2.COLOR_GRAY2BGR)

        # Perform OCR using EasyOCR
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(preprocessed_img)

        # Extract text from OCR results
        extracted_text = "\n".join([detection[1] for detection in result])
        for detection in result:
            top_left, bottom_right = tuple(map(int, detection[0][0])), tuple(map(int, detection[0][2]))
            preprocessed_img_bgr = cv2.rectangle(preprocessed_img_bgr, top_left, bottom_right, (0, 255, 0), 2)

        # Schedule background tasks for saving files
        asyncio.create_task(save_file_async(TEMP_IMAGE_PATH, preprocessed_img_bgr, is_image=True))
        asyncio.create_task(save_file_async(TEXT_FILE_PATH, extracted_text))

        print(f"Background tasks started for saving files.")
        return extracted_text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
