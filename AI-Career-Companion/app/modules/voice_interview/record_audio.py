import tempfile
import shutil

def save_uploaded_audio(uploaded_file, extension=".wav"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
        shutil.copyfileobj(uploaded_file, tmp)
        return tmp.name
def save_audio_from_bytes(audio_bytes, extension=".wav"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
        tmp.write(audio_bytes)
        return tmp.name
# record_audio.py

import os
from pydub import AudioSegment

def convert_to_proper_wav(input_path, target_sample_rate=16000):
    """
    Converts an audio file to WAV format with proper encoding:
    - PCM 16-bit
    - Mono
    - 16kHz sample rate
    """
    # Guess format based on file extension
    ext = os.path.splitext(input_path)[1].replace(".", "")
    if ext.lower() not in ["webm", "ogg", "wav", "mp3", "m4a"]:
        raise ValueError(f"Unsupported audio format: {ext}")

    try:
        # Load with pydub
        audio = AudioSegment.from_file(input_path, format=ext)
        audio = audio.set_frame_rate(target_sample_rate).set_channels(1)

        # Output path
        output_path = input_path.replace(f".{ext}", ".wav")

        # Export as proper PCM WAV
        audio.export(output_path, format="wav", codec="pcm_s16le")
        return output_path

    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {e}")
