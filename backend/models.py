# backend/models.py

from pydantic import BaseModel

class SynthesizeRequest(BaseModel):
    """
    Represents a request to synthesize speech.

    Attributes:
        text (str): The text to be synthesized into speech.
        language (str): The language of the text.
        voice_file (str): The voice file name to use as a reference during the synthesis.
    """
    text: str
    language: str
    voice_file: str
