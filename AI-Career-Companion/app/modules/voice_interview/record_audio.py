import os
import uuid
import shutil

def save_uploaded_audio(file_obj, extension=".webm", save_dir="temp_audio"):
    os.makedirs(save_dir, exist_ok=True)
    filename = f"uploaded_{uuid.uuid4().hex[:8]}{extension}"
    path = os.path.join(save_dir, filename)
    with open(path, "wb") as out_file:
        shutil.copyfileobj(file_obj, out_file)

    return path