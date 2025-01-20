import easyocr
import cv2
from helper.imagePreProcessor import preprocess_image 

def extract_text_from_image(image_path):
    try:
        preprocessed_img = preprocess_image(image_path)
        if preprocessed_img is None:
            raise ValueError("Preprocessing failed.")

        preprocessed_img_bgr = cv2.cvtColor(preprocessed_img, cv2.COLOR_GRAY2BGR)
        temp_image_path = f"./static/temp_preprocessed_image.jpg"
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(preprocessed_img)

        extracted_text = "\n".join([detection[1] for detection in result])
        for detection in result:
            top_left, bottom_right = tuple(map(int, detection[0][0])), tuple(map(int, detection[0][2]))
            preprocessed_img_bgr = cv2.rectangle(preprocessed_img_bgr, top_left, bottom_right, (0, 255, 0), 2)

        # await asyncio.gather(
        #     save_file_async(temp_image_path, preprocessed_img_bgr, is_image=True),
        #     save_file_async("./static/extracted_data.txt", extracted_text)
        # )
        # print(f"Saved processed image: {temp_image_path}")
        # print(f"Saved text: ./static/extracted_data.txt")
        return extracted_text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
