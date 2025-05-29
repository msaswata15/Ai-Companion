import requests
import time
import os
from app.utils import settings # assumes your Settings class loads ASSEMBLY_API_KEY
import mimetypes
ASSEMBLY_API_KEY = settings.assembly_api_key

def transcribe_audio(file_path: str) -> str:
    """Upload an audio file to AssemblyAI and return the transcript text."""

    print(f"[DEBUG] MIME type: {mimetypes.guess_type(file_path)}")
    print(f"[DEBUG] File size before upload: {os.path.getsize(file_path)}")
    headers = {"authorization": ASSEMBLY_API_KEY}
    # Upload audio
    with open(file_path, "rb") as f:
        response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, files={"file": f})
    audio_url = response.json()["upload_url"]

    # Start transcription
    json_payload = {
        "audio_url": audio_url,
        "auto_chapters": False,
        "speaker_labels": False
    }
    transcript_response = requests.post("https://api.assemblyai.com/v2/transcript", json=json_payload, headers=headers)
    transcript_id = transcript_response.json()["id"]

    # Poll until transcription is done
    while True:
        poll = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers).json()
        if poll["status"] == "completed":
            return poll["text"]
        elif poll["status"] == "error":
            raise Exception(f"Transcription failed: {poll['error']}")
        time.sleep(2)
