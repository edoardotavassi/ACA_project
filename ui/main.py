import streamlit as st
import numpy as np
import json
import requests
from io import BytesIO
from pydub import AudioSegment

st.title('ACA TTS Demo')

st.write('This is a demo of the ACA TTS model. You can use this app to generate speech from text.')

# Fetch the list of available voice files
response = requests.get("http://127.0.0.1:8000/voices")
if response.status_code == 200:
    voice_files = response.json().get("voices", [])
else:
    st.error("Failed to fetch the list of voice files.")
    voice_files = []

# File upload
uploaded_file = st.file_uploader("Choose a WAV file", type="wav")
if uploaded_file is not None:
    files = {'file': uploaded_file.getvalue()}
    response = requests.post("http://127.0.0.1:8000/upload", files=files)
    if response.status_code == 200:
        st.success(f"File '{uploaded_file.name}' uploaded successfully.")
        voice_files.append(uploaded_file.name)
    else:
        st.error("Failed to upload the file.")

# Text input area
text = st.text_area('Text to synthesize', 'Antonio Conte è pronto a tornare in Italia. Tre anni dopo il suo addio all’Inter, il tecnico leccese secondo le indiscrezioni è infatti pronto a firmare un nuovo accordo con il Napoli, che dopo una stagione burrascosa chiusa con il decimo posto in classifica vuole subito rialzarsi e tornare a lottare per le posizioni di vertice.')

# Language selection dropdown
language = st.selectbox('Language', [
    'en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh-cn', 'ja', 'hu', 'ko', 'hi'
])

# Voice file selection dropdown
voice_file = st.selectbox('Voice File', voice_files)

# Synthesize button
synth_button = st.button('Synthesize')

# Audio placeholder
audio_placeholder = st.empty()

# If the synthesize button is pressed
if synth_button:
    # Create a dictionary of the current state
    data = {
        'text': text,
        'language': language,
        'voice_file': voice_file,
    }
    # Convert the dictionary to a JSON string
    json_data = json.dumps(data, indent=4)
    
    # Display the JSON string in the debug text area
    st.text_area("debug", value=json_data, height=200)
    
    # Send the JSON data to the FastAPI backend
    response = requests.post("http://127.0.0.1:8000/synthesize", json=data)
    
    if response.status_code == 200:
        # Get the MP3 data from the response
        mp3_data = response.content
        
        # Convert MP3 to AudioSegment
        audio_segment = AudioSegment.from_mp3(BytesIO(mp3_data))
        
        # Ensure the sample rate is 24000 Hz
        audio_segment = audio_segment.set_frame_rate(24000)
        
        # Convert AudioSegment to raw audio data
        raw_data = np.array(audio_segment.get_array_of_samples())
               
        # Update the audio player with the new audio data
        st.audio(BytesIO(mp3_data), format='audio/mp3')
    else:
        st.error("Failed to synthesize audio. Please try again.")
else:
    # Display an empty debug text area when the button is not pressed
    st.text_area("debug", value="", height=200)
