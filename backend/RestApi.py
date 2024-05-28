import uvicorn
from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List
from pydub import AudioSegment
import numpy as np
import lameenc
import io
import os
from TTS.api import TTS

app = FastAPI()  # definition of framework

# name of the app framework
@app.get("/", status_code=200)
def root():
    return {"ACA_PROJECT"}

# health check that return the status with 200 code
@app.get("/health_check", status_code=200)
def health_check():
    return {"Status": "OK"}

# if the user insert an empty string we handle this situation as an exception
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"status": "Error"}),
    )

class SynthesizeRequest(BaseModel):
    text: str
    language: str
    voice_file: str

def split_text(text, max_length=200):
    words = text.split()
    current_chunk = []
    chunks = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_chunk) > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def encode_wav_to_mp3(wav_data_array, sample_rate=24000):
    def float32_to_pcm16(float32_array):
        float32_array = np.clip(float32_array, -1.0, 1.0)
        int16_array = (float32_array * 32767).astype(np.int16)
        return int16_array

    pcm16_array = float32_to_pcm16(wav_data_array)
    wav_data = pcm16_array.tobytes()
    
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(128)
    encoder.set_in_sample_rate(sample_rate)
    encoder.set_channels(1 if len(wav_data_array.shape) == 1 else wav_data_array.shape[1])
    encoder.set_quality(2)

    mp3_data = encoder.encode(wav_data)
    mp3_data += encoder.flush()

    return mp3_data

@app.get("/voices")
async def list_voices():
    voice_files = [f for f in os.listdir("input") if f.endswith(".wav")]
    return {"voices": voice_files}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"input/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.post("/synthesize")
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

# classic main method
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
