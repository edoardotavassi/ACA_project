# ui/ui.py

import streamlit as st
from io import BytesIO
from pydub import AudioSegment
import numpy as np
from api import upload_voice_file, synthesize_speech

def show_title():
    st.title('ACA TTS Demo')

def show_description():
    st.write('This is a demo of the ACA TTS model. You can use this app to generate speech from text.')

def show_voice_file_uploader():
    uploaded_file = st.file_uploader("Choose a WAV file", type="wav")
    if uploaded_file is not None:
        response = upload_voice_file(uploaded_file)
        if response.status_code == 200:
            st.success(f"File '{uploaded_file.name}' uploaded successfully.")
            return uploaded_file.name
        else:
            st.error("Failed to upload the file.")
    return None

def show_text_input():
    return st.text_area('Text to synthesize', 'Antonio Conte è pronto a tornare in Italia. Tre anni dopo il suo addio all’Inter, il tecnico leccese secondo le indiscrezioni è infatti pronto a firmare un nuovo accordo con il Napoli, che dopo una stagione burrascosa chiusa con il decimo posto in classifica vuole subito rialzarsi e tornare a lottare per le posizioni di vertice.')

def show_language_selector():
    return st.selectbox('Language', [
        'en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh-cn', 'ja', 'hu', 'ko', 'hi'
    ])

def show_voice_file_selector(voice_files):
    return st.selectbox('Voice File', voice_files)

def show_synthesize_button():
    return st.button('Synthesize')

def show_debug_area(json_data):
    st.text_area("debug", value=json_data, height=200)

def show_audio_player(mp3_data):
    st.audio(BytesIO(mp3_data), format='audio/mp3')

def display_synthesis_result(mp3_data):
    # Convert MP3 to AudioSegment
    audio_segment = AudioSegment.from_mp3(BytesIO(mp3_data))
    
    # Ensure the sample rate is 24000 Hz
    audio_segment = audio_segment.set_frame_rate(24000)
    
    # Convert AudioSegment to raw audio data
    raw_data = np.array(audio_segment.get_array_of_samples())
    
    # Update the audio player with the new audio data
    show_audio_player(mp3_data)
