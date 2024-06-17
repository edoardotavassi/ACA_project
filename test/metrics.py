import requests
import time
import os
import pandas as pd
import re

# Define the URL for the backend endpoint
URL = "http://localhost:8000/synthesize"

# Define the path to save the returned audio files
SAVE_PATH = "synthesized_audio/"
# Path to save response times
RESPONSE_TIMES_PATH = os.path.join(SAVE_PATH, "response_times.csv")

def extract_filename(path):
    """
    Extracts the filename from a given path.

    Args:
        path (str): The path from which to extract the filename.

    Returns:
        str: The extracted filename, or None if no filename is found.
    """
    match = re.search(r'[^/]+$', path)
    return match.group(0) if match else None

def test_synthesize(text, voice_file, language="en"):
    """
    Synthesizes audio from the given text using the specified voice file and language.

    Args:
        text (str): The text to synthesize into audio.
        voice_file (str): The path to the voice file to use for synthesis.
        language (str, optional): The language code for the text. Defaults to "en".

    Returns:
        float: The response time in seconds.
    """
    data = {
        'text': text,
        'language': language,
        'voice_file': voice_file,
    }
    
    # Measure the start time
    start_time = time.time()
    
    # Send the POST request to the backend
    response = requests.post(URL, json=data)
    
    # Measure the end time
    end_time = time.time()
    
    # Calculate the response time
    response_time = end_time - start_time
    print(f"Response time: {response_time:.2f} seconds")
    
    # Save the returned audio file
    if response.status_code == 200:
        audio_filename = os.path.join(SAVE_PATH, f"{voice_file}_{int(start_time)}.mp3")
        with open(audio_filename, "wb") as f:
            f.write(response.content)
        print(f"Audio file saved as: {audio_filename}")
    else:
        print(f"Failed to synthesize audio. Status code: {response.status_code}, Response: {response.text}")
    
    return response_time

# Ensure the save path directory exists
os.makedirs(SAVE_PATH, exist_ok=True)

# Load the CSV data
csv_file_path = "/mnt/data/validated_clips.csv"
df = pd.read_csv(csv_file_path)

# Initialize response times DataFrame if it does not exist
if not os.path.exists(RESPONSE_TIMES_PATH):
    response_times_df = pd.DataFrame(columns=['voice_file', 'response_time'])
    response_times_df.to_csv(RESPONSE_TIMES_PATH, index=False)
else:
    response_times_df = pd.read_csv(RESPONSE_TIMES_PATH)

# Iterate over the rows in the CSV and test each one
for index, row in df.iterrows():
    text = row['sentence']  # Replace with the actual column name if different
    voice_file_path = row['path']  # Replace with the actual column name if different
    
    voice_file = extract_filename(voice_file_path)
    
    response_time = test_synthesize(text, voice_file)
    
    # Append response time to the CSV file
    new_row = pd.DataFrame({'voice_file': [voice_file], 'response_time': [response_time]})
    new_row.to_csv(RESPONSE_TIMES_PATH, mode='a', header=False, index=False)

print("Completed synthesizing audio for all entries in the CSV.")