from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

sentence="È passato un anno da quando Batman ha fatto la sua comparsa e Gotham City è diventata un posto migliore, con la malavita terrorizzata, ma anche con alcuni vigilanti improvvisati che cercano in tutti i modi di imitare l'Uomo Pipistrello, il quale disapprova un simile operato e fa capire di non poter condividere la sua missione con "
voice_to_clone="input/it.wav"
output_name="output.wav"

# generate speech by cloning a voice using default settings
tts.tts_to_file(text=sentence,
                file_path=output_name,
                speaker_wav=voice_to_clone,
                language="it")
