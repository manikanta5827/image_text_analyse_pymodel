
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import asyncio
from concurrent.futures import ThreadPoolExecutor

# async def save_file_async(file_path, data, is_image=False):
#     loop = asyncio.get_event_loop()
#     with ThreadPoolExecutor() as pool:
#         await loop.run_in_executor(pool, lambda: cv2.imwrite(file_path, data) if is_image else open(file_path, "w").write(data))

def preprocess_image(image_path):
    try:
        img = Image.open(image_path).convert("L")
        img = ImageOps.autocontrast(img).filter(ImageFilter.SHARPEN)
        return np.array(img)
    except Exception as e:
        print(f"Preprocessing Error: {e}")
        return None


