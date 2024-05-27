import streamlit as st
import numpy as np

st.title('ACA TTS Demo')

st.write('This is a demo of the ACA TTS model. You can use this app to generate speech from text.')

text = st.text_area('Text to synthesize', 'Hello, how are you?')
language = st.selectbox('Language', ['en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh-cn', 'ja', 'hu', 'ko', 'hi'])
synth_button = st.button('Synthesize')
audio = st.audio(np.load('out.npy'), sample_rate=22100, format='audio/wav')

if synth_button:
    audio

