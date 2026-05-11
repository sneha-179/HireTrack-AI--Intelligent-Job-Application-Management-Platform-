import os
from fastapi import HTTPException

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_resume(file_bytes, filename):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        url = f"http://localhost:8000/uploads/{filename}"
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


def get_presigned_url(filename):
    try:
        url = f"http://localhost:8000/uploads/{filename}"
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not generate URL: {str(e)}")


def delete_resume(filename):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not delete file: {str(e)}")