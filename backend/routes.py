# backend/routes.py

from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
import os
import io
import numpy as np
from typing import List

from models import SynthesizeRequest
from utils import split_text, encode_wav_to_mp3
from TTS.api import TTS

router = APIRouter()



@router.get("/voices")
async def list_voices():
    voice_files = [f for f in os.listdir("input") if f.endswith(".wav")]
    return {"voices": voice_files}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"input/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@router.post("/synthesize")
async def synthesize(request: SynthesizeRequest):
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
    voice_to_clone = f"input/{request.voice_file}"
    text_chunks = split_text(request.text)
    synthesized_audio = []

    for chunk in text_chunks:
        wav = tts.tts(text=chunk, speaker_wav=voice_to_clone, language=request.language)
        synthesized_audio.append(np.array(wav))

    concatenated_audio = np.concatenate(synthesized_audio)
    mp3_data = encode_wav_to_mp3(concatenated_audio)

    # Use an in-memory bytes buffer
    mp3_buffer = io.BytesIO(mp3_data)

    return StreamingResponse(mp3_buffer, media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=output.mp3"})
