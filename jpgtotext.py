import requests
from config import api_token


def image_detect(image):  
    files = {'image': image}  
    headers = {'X-Api-Key': f"{api_token}"}  
    try:  
        response = requests.post('https://api.api-ninjas.com/v1/imagetotext', headers=headers, files=files)  
        if response.status_code == 200:  
            print("Hammasi joyida")
            uzunligi=len(response.json())
            text=""
            for i in range(uzunligi):
                text+=f"{response.json()[i]['text']} "
            return text
        else:  
            return f"Xatolik: {response.status_code}, {response.text}"  
    except Exception as e:  
        return f"Xatolik: {e}"  
# sudo apt update  
# sudo apt install tesseract-ocr
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
