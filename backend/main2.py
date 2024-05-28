from pydub import AudioSegment
import numpy as np
import lameenc
from IPython.display import Audio

from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

sentence="È passato un anno da quando Batman ha fatto la sua comparsa e Gotham City è diventata un posto migliore, con la malavita terrorizzata, ma anche con alcuni vigilanti improvvisati che cercano in tutti i modi di imitare l'Uomo Pipistrello, il quale disapprova un simile operato e fa capire di non poter condividere la sua missione con "
voice_to_clone="input/it.wav"
output_name="output.wav"

# generate speech by cloning a voice using default settings
wav=tts.tts(text=sentence,
                speaker_wav=voice_to_clone,
                language="it")


print(isinstance(wav, np.ndarray))



def encode_wav_to_mp3(wav_data_array, sample_rate=22100):

    def float32_to_pcm16(float32_array):
        """
        Convert numpy array of float32 to PCM 16-bit format.
        """
        # Ensure the array is within the correct range
        float32_array = np.clip(float32_array, -1.0, 1.0)
        # Convert to PCM 16-bit
        int16_array = (float32_array * 32767).astype(np.int16)
        return int16_array

    # Convert the float32 array to PCM 16-bit format
    pcm16_array = float32_to_pcm16(wav_data_array)
    
    # Convert the PCM 16-bit array to bytes
    wav_data = pcm16_array.tobytes()
    
    # Initialize the MP3 encoder
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(128)
    encoder.set_in_sample_rate(sample_rate)
    encoder.set_channels(1 if len(wav_data_array.shape) == 1 else wav_data_array.shape[1])
    encoder.set_quality(2)  # 2-highest, 7-fastest

    # Encode the WAV data to MP3
    mp3_data = encoder.encode(wav_data)
    mp3_data += encoder.flush()

    return mp3_data

mp3=encode_wav_to_mp3(wav)


with open("output.mp3", "wb") as f:
    f.write(mp3)
