import pvporcupine
import sounddevice as sd

def listen_for_wake_word():
    porcupine = pvporcupine.create(keywords=["jarvis"])
    
    with sd.InputStream(channels=1, samplerate=porcupine.sample_rate, blocksize=porcupine.frame_length) as stream:
        while True:
            audio_frame, _ = stream.read(porcupine.frame_length)
            keyword_index = porcupine.process(audio_frame[:, 0])

            if keyword_index >= 0:
                print("Wake word detected")
                return True
