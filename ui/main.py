# ui/main.py

import streamlit as st
import json
from ui import (
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
from api import get_voice_files, synthesize_speech

def main():
    """
    Main function that orchestrates the speech synthesis application.

    This function performs the following steps:
    1. Shows the title and description.
    2. Fetches the list of available voice files.
    3. Shows the voice file uploader and appends the uploaded file name to the voice files list if a file is uploaded.
    4. Gets user input for text, language, and voice file.
    5. Shows the synthesis button.
    6. If the synthesis button is clicked, collects input data, displays it in the debug area, and performs speech synthesis.
    7. If synthesis is successful, displays the synthesized audio result.
    8. If synthesis fails, displays an error message.
    9. If the synthesis button is not clicked, clears the debug area.
    """
    # Show the title and description
    show_title()
    show_description()

    # Fetch the list of available voice files
    voice_files = get_voice_files()
    uploaded_file_name = show_voice_file_uploader()
    
    if uploaded_file_name:
        voice_files.append(uploaded_file_name)

    # Get user input for text, language, and voice file
    text = show_text_input()
    language = show_language_selector()
    voice_file = show_voice_file_selector(voice_files)
    synth_button = show_synthesize_button()

    # If the synthesis button is clicked
    if synth_button:
        # Collect input data and display in debug area
        data = {
            'text': text,
            'language': language,
            'voice_file': voice_file,
        }
        json_data = json.dumps(data, indent=4)
        #show_debug_area(json_data)
        
        # Perform speech synthesis
        response = synthesize_speech(data)
        
        # If synthesis is successful, display the result
        if response.status_code == 200:
            mp3_data = response.content
            display_synthesis_result(mp3_data)
        else:
            # If synthesis fails, display error message
            st.error("Failed to synthesize audio. Please try again.")

if __name__ == "__main__":
    main()
