import os
import io
import shutil
import fitz
from PIL import Image
from cat.log import log
import base64

OUTPUT_IMAGES = "output_images"

def split_pdf(input_pdf):
    try:
        if not os.path.exists(OUTPUT_IMAGES):
            os.makedirs(OUTPUT_IMAGES)
        doc = fitz.open(stream=input_pdf, filetype="pdf")
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap()

            img_bytes = pix.tobytes("png")
            img_buffer = io.BytesIO(img_bytes)
            img = Image.open(img_buffer)

            img_path = os.path.join(OUTPUT_IMAGES, f"page_{i+1}.png")
            img.save(img_path)
        doc.close()
        return True
    except Exception as e:
        log.error(f"Error during split_pdf: {e}")
        return False

def read_images():
    images_data = []
    try:
        for filename in os.listdir(OUTPUT_IMAGES):
            if filename.lower().endswith('.png'):
                image_path = os.path.join(OUTPUT_IMAGES, filename)
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(
                        image_file.read()).decode("utf-8")
                    images_data.append(encoded_image)
        return images_data
    except Exception as e:
        log.error(f"Error during read_images: {e}")
        return None
    
def clear_images():
    try:
        if os.path.exists(OUTPUT_IMAGES):
            shutil.rmtree(OUTPUT_IMAGES)
            log.info("output_images folder and its contents have been deleted.")
    except Exception as e:
        log.error(f"Error during clear_images: {e}")
