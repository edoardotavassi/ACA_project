import streamlit as st
import numpy as np
import json

st.title('ACA TTS Demo')

st.write('This is a demo of the ACA TTS model. You can use this app to generate speech from text.')

# Text input area
text = st.text_area('Text to synthesize', 'Hello, how are you?')

# Language selection dropdown
language = st.selectbox('Language', [
    'en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh-cn', 'ja', 'hu', 'ko', 'hi'
])

# Synthesize button
synth_button = st.button('Synthesize')

# Audio placeholder
audio = st.audio("it.wav", format="audio/wav")

# If the synthesize button is pressed
if synth_button:
    # Create a dictionary of the current state
    data = {
        'text': text,
        'language': language,
    }
    # Convert the dictionary to a JSON string
    json_data = json.dumps(data, indent=4)
    # Display the JSON string in the debug text area
    st.text_area("debug", value=json_data, height=200)
else:
    # Display an empty debug text area when the button is not pressed
    st.text_area("debug", value="", height=200)

