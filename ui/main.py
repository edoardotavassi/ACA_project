# ui/main.py

import streamlit as st
from .ui import (
    show_title,
    show_description,
    show_voice_file_uploader,
    show_text_input,
    show_language_selector,
    show_voice_file_selector,
    show_synthesize_button,
    show_debug_area,
    display_synthesis_result
)
from .api import get_voice_files, synthesize_speech

def main():
    show_title()
    show_description()

    # Fetch the list of available voice files
    voice_files = get_voice_files()
    uploaded_file_name = show_voice_file_uploader()
    
    if uploaded_file_name:
        voice_files.append(uploaded_file_name)

    text = show_text_input()
    language = show_language_selector()
    voice_file = show_voice_file_selector(voice_files)
    synth_button = show_synthesize_button()

    if synth_button:
        data = {
            'text': text,
            'language': language,
            'voice_file': voice_file,
        }
        json_data = json.dumps(data, indent=4)
        show_debug_area(json_data)
        
        response = synthesize_speech(data)
        
        if response.status_code == 200:
            mp3_data = response.content
            display_synthesis_result(mp3_data)
        else:
            st.error("Failed to synthesize audio. Please try again.")
    else:
        show_debug_area("")

if __name__ == "__main__":
    main()
