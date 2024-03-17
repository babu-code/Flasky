import requests
from app.config import Config

def translate(text ,source_lang, dest_lang,api_key=Config.TRANSLATOR_KEY):
    base_url = "http://mymemory.translated.net/api/get"
    params = {
        "q": text,
        "langpair": f"{source_lang}|{dest_lang}",
        "key":api_key 
    }
    response = requests.get(base_url, params=params)
    translated_data = response.json()
    translated_text = translated_data["responseData"]["translatedText"]
    return translated_text