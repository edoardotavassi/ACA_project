# ui/api.py

import requests

BASE_URL = "http://127.0.0.1:8000"

def get_voice_files():
    """
    Retrieves a list of voice files from the API.

    Returns:
        A list of voice files, or an empty list if the request fails or no voice files are found.
    """
    response = requests.get(f"{BASE_URL}/voices")
    if response.status_code == 200:
        return response.json().get("voices", [])
    else:
        return []

def upload_voice_file(file):
    """
    Uploads a voice file to the server.

    Args:
        file: A file object representing the voice file to be uploaded.

    Returns:
        The response object returned by the server after the upload.

    Raises:
        Any exceptions raised by the requests.post() method.
    """
    files = {'file': file.getvalue()}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    return response

def synthesize_speech(data):
    """
    Send the data to the server to synthesize.

    Args:
        data (dict): The data to be used for speech synthesis.

    Returns:
        Response: The response audio from the API request.

    """
    response = requests.post(f"{BASE_URL}/synthesize", json=data)
    return response
