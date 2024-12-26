import requests
import urllib3
from config import ttsurl

def texttospeech(message):
    try:	
        headers = {"Content-Type": "application/json"} 
        data = {"text": message}
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

        response = requests.post(ttsurl, headers=headers, json=data, verify=False)

        if response.status_code==200:
            return response.content
        else:
            return response.status_code
    except Exception as e:
        return f"<u>Xatolik sodir bo'ldi:</u>\n<code>{e}</code>"