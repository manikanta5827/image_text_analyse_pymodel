import easyocr
import cv2
from helper.imagePreProcessor import preprocess_image 
import os
import re

# Base directory for the backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../static'))
TEMP_IMAGE_PATH = os.path.join(STATIC_DIR, 'temp_preprocessed_image.jpg')
TEXT_FILE_PATH = os.path.join(STATIC_DIR, 'extracted_data.txt')

# Ensure the static directory exists
os.makedirs(STATIC_DIR, exist_ok=True)

def save_file(path, content, is_image=False):
    if is_image:
        cv2.imwrite(path, content) 
    else:
        with open(path, 'w') as f:
            f.write(content)  # Save text

# import re

def format_extracted_text(text):
    lines = text.strip().split("\n")  # Split text into lines
    formatted_lines = []
    temp_line = ""  # Temporary variable to hold food item names

    for line in lines:
        # Remove all special characters except letters, numbers, and spaces
        line = re.sub(r'[^A-Za-z0-9\s]', '', line)

        # If 's' or 'S' appears before a number, add a space before the number and remove the 's'/'S'
        line = re.sub(r'[sS](\d)', r' \1', line)

        # Check if it's a price (integer or decimal)
        if re.match(r'^\d+(\.\d{1,2})?$', line):  
            # If it's a four-digit number, remove the first digit
            line = re.sub(r'^(\d)(\d{3})$', r'\2', line)  

            temp_line += " " + line  # Attach price to the previous food item
            formatted_lines.append(temp_line)  # Store the complete food-price pair
            temp_line = ""  # Reset storage
        else:
            if temp_line:  # If a previous food item is pending
                formatted_lines.append(temp_line)  # Save it before starting a new one
            temp_line = line  # Start a new food item entry

    if temp_line:  # In case the last line was a food name without a price
        formatted_lines.append(temp_line)

    return "\n".join(formatted_lines)  # Join back as formatted text

def extract_text_from_image(image_path):
    try:
        # Preprocess the image
        preprocessed_img = preprocess_image(image_path)
        if preprocessed_img is None:
            raise ValueError("Preprocessing failed.")

        # Convert grayscale image back to BGR for visualization
        preprocessed_img_bgr = cv2.cvtColor(preprocessed_img, cv2.COLOR_GRAY2BGR)

        # Perform OCR using EasyOCR
        reader = easyocr.Reader(['en'], gpu=True)
        result = reader.readtext(preprocessed_img)

        # Extract text from OCR results
        extracted_text = "\n".join([detection[1] for detection in result])

        # Format the extracted text
        formatted_text = format_extracted_text(extracted_text)

        # Draw bounding boxes around detected text
        for detection in result:
            top_left, bottom_right = tuple(map(int, detection[0][0])), tuple(map(int, detection[0][2]))
            preprocessed_img_bgr = cv2.rectangle(preprocessed_img_bgr, top_left, bottom_right, (0, 255, 0), 2)

        # Save processed image and formatted text
        save_file(TEMP_IMAGE_PATH, preprocessed_img_bgr, is_image=True)
        save_file(TEXT_FILE_PATH, formatted_text)

        print("OCR completed successfully.")
        return formatted_text
    except Exception as e:
        print(f"Error in [textExtractor.py] OCR Error: {e}")
        return ""
