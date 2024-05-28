# backend/models.py

from pydantic import BaseModel

class SynthesizeRequest(BaseModel):
    text: str
    language: str
    voice_file: str
