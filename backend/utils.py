# backend/utils.py

import numpy as np
import lameenc

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
