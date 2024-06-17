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

def show_text_input():
    return st.text_area('Text to synthesize', '')

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

def show_voice_file_uploader():
    """
    Displays a file uploader widget for selecting a WAV file and uploads it.

    Returns:
        str or None: The name of the uploaded file if successful, None otherwise.
    """
    # Display a file uploader widget for selecting a WAV file
    uploaded_file = st.file_uploader("Choose a WAV file", type="wav")
    
    if uploaded_file is not None:
        # Upload the file using the upload_voice_file function from the api module
        response = upload_voice_file(uploaded_file)
        
        # If the file is uploaded successfully
        if response.status_code == 200:
            st.success(f"File '{uploaded_file.name}' uploaded successfully.")
            return uploaded_file.name
        else:
            # Display an error message if the file upload fails
            st.error("Failed to upload the file.")
    
    # Return None if no file is uploaded
    return None

def display_synthesis_result(mp3_data):
    """
    Display the synthesis result by converting MP3 data to an AudioSegment,
    adjusting the sample rate to 24000 Hz, converting it to raw audio data,
    and updating the audio player with the new audio data.

    Parameters:
    - mp3_data (bytes): The MP3 data to be displayed.
    """
    # Convert MP3 to AudioSegment
    audio_segment = AudioSegment.from_mp3(BytesIO(mp3_data))
    
    # Ensure the sample rate is 24000 Hz
    audio_segment = audio_segment.set_frame_rate(24000)
    
    # Convert AudioSegment to raw audio data
    raw_data = np.array(audio_segment.get_array_of_samples())
    
    # Update the audio player with the new audio data
    show_audio_player(mp3_data)
