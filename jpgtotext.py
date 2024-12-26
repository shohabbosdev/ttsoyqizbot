from PIL import Image
import pytesseract
import re

def clean_text(text):
    text = text.replace("\n",' ')
    return re.sub(r'[^a-zA-Z0-9\s,.!?]', '', text)

def jpgtotext(image):
    try:
        image = Image.open(image)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 
        text = pytesseract.image_to_string(image)
        return clean_text(text)
    except Exception as e:
        return f"Xatolik xabari: {e}"
# sudo apt update  
# sudo apt install tesseract-ocr
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'