import easyocr
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import os

def extract_text_from_image(image_path):
    try:
        # Initialize EasyOCR Reader
        reader = easyocr.Reader(['en'], gpu=True)

        # Perform OCR
        result = reader.readtext(image_path)

        # Load the image with OpenCV
        img = cv2.imread(image_path)

        # Convert the OpenCV image to a Pillow image for preprocessing
        pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # Convert to grayscale
        pil_image = pil_image.convert("L")

        # Enhance contrast
        pil_image = ImageOps.autocontrast(pil_image)

        # Apply sharpening filter
        pil_image = pil_image.filter(ImageFilter.SHARPEN)

        # Convert the preprocessed Pillow image back to OpenCV format
        img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_GRAY2BGR)

        # Prepare a list to hold the extracted text
        extracted_texts = []

        # Loop through all detected text regions
        for detection in result:
            top_left = tuple(map(int, detection[0][0]))  # Top-left corner of the bounding box
            bottom_right = tuple(map(int, detection[0][2]))  # Bottom-right corner of the bounding box
            text = detection[1]  # Detected text

            # Draw a rectangle around the text
            img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

            # Append the text and confidence to the list
            extracted_texts.append(text)

        # Join all the extracted text into a single string separated by commas
        extracted_text = ", ".join(extracted_texts)

        # Save the processed image with [processed] appended to the original filename
        base, ext = os.path.splitext(image_path)
        processed_image_path = f"{base}_processed{ext}"
        cv2.imwrite(processed_image_path, img)

        print(f"Processed image saved to: {processed_image_path}")
        with open("output.txt", "w") as file:
           file.write(extracted_text)
        # Return the extracted text
        return extracted_text
    except Exception as e:
        print(f"Error in extracting text from image: {e}")
        return ""
