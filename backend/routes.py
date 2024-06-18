# backend/routes.py

from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
import os
import io
import numpy as np
import shutil
from typing import List

from models import SynthesizeRequest
from utils import split_text, encode_wav_to_mp3
from TTS.api import TTS

router = APIRouter()



@router.get("/voices")
async def list_voices():
    """
    Retrieve a list of voice files.

    Returns:
        dict: A dictionary containing the list of voice files.
    """
    voice_files = [f for f in os.listdir("input") if f.endswith(".wav")]
    return {"voices": voice_files}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to the server.

    Parameters:
    - file: The file to be uploaded.

    Returns:
    - A dictionary containing information about the uploaded file.
    """
    # Ensure the input directory exists
    os.makedirs("input", exist_ok=True)
    
    # Construct the file path with the original filename and extension
    file_location = os.path.join("input", file.filename)


    # Open the file in binary write mode
    with open(file_location, "wb") as f:
        # Write the contents of the uploaded file to the file location using shutil.copyfileobj
        shutil.copyfileobj(file.file, f)

    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@router.post("/delete_file")
async def delete_file(file: str):
    """
    Deletes a file from the 'input' directory.

    Args:
        file (str): The name of the file to be deleted.

    Returns:
        dict: A dictionary containing information about the deletion process.

    Raises:
        HTTPException: If the file is not found in the 'input' directory.
    """
    file_location = f"input/{file}"
    
    # Check if the file exists
    if os.path.exists(file_location):
        # If the file exists, remove it
        os.remove(file_location)
        return {"info": f"file '{file}' deleted"}
    else:
        # If the file does not exist, raise an HTTPException with a 404 status code and a detail message
        raise HTTPException(status_code=404, detail="File not found")

@router.post("/synthesize")
async def synthesize(request: SynthesizeRequest):
    """
    Synthesizes audio from text using a TTS model.

    Args:
        request (SynthesizeRequest): The request object containing the text, voice file, and language.

    Returns:
        StreamingResponse: The synthesized audio as an MP3 file.

    Raises:
        None
    """
    # Create an instance of the TTS model
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
    tts.to(0)
    voice_to_clone = f"input/{request.voice_file}"

    # Split the text into smaller chunks to avoid exceeding the model's maximum input length
    text_chunks = split_text(request.text)

    # Initialize an empty list to store the synthesized audio chunks
    synthesized_audio = []

    # Iterate over each text chunk
    for chunk in text_chunks:
        # Synthesize audio for the current chunk using the TTS model
        wav = tts.tts(text=chunk, speaker_wav=voice_to_clone, language=request.language)
        synthesized_audio.append(np.array(wav))

    # Concatenate the synthesized audio chunks into a single array
    concatenated_audio = np.concatenate(synthesized_audio)

    # Encode the concatenated audio as an MP3 file
    mp3_data = encode_wav_to_mp3(concatenated_audio)

    # Create an in-memory bytes buffer to store the MP3 data
    mp3_buffer = io.BytesIO(mp3_data)

    # Return the synthesized audio as a streaming response with the appropriate media type and headers
    return StreamingResponse(mp3_buffer, media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=output.mp3"})
