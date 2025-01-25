import numpy as np
from PIL import Image, ImageFilter, ImageOps
def preprocess_image(image_path):
    try:
        img = Image.open(image_path).convert("L")
        img = ImageOps.autocontrast(img).filter(ImageFilter.SHARPEN)
        return np.array(img)
    except Exception as e:
        print(f"Error [ in imagePreProcessor file ] Preprocessing Error: {e}")
        return None
