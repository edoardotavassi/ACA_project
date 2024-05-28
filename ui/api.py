# ui/api.py

import requests

BASE_URL = "http://127.0.0.1:8000"

def get_voice_files():
    response = requests.get(f"{BASE_URL}/voices")
    if response.status_code == 200:
        return response.json().get("voices", [])
    else:
        return []

def upload_voice_file(file):
    files = {'file': file.getvalue()}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    return response

def synthesize_speech(data):
    response = requests.post(f"{BASE_URL}/synthesize", json=data)
    return response
