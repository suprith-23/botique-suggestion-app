import os
import shutil
from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.core.config import get_settings
from PIL import Image
import io

settings = get_settings()


def ensure_upload_dir():
    """Ensure uploads directory exists"""
    os.makedirs(settings.uploads_dir, exist_ok=True)


async def save_upload_file(file: UploadFile, user_id: int) -> str:
    """Save uploaded file"""
    
    ensure_upload_dir()
    
    # Check file size
    contents = await file.read()
    if len(contents) > settings.max_upload_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.max_upload_size / (1024*1024)}MB"
        )
    
    # Check file type
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: JPG, PNG, WebP"
        )
    
    # Verify it's actually an image
    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file"
        )
    
    # Generate filename
    filename = f"user_{user_id}_{int(os.path.getmtime(__file__))}_{file.filename}"
    filepath = os.path.join(settings.uploads_dir, filename)
    
    # Save file
    with open(filepath, "wb") as f:
        f.write(contents)
    
    return filepath


def delete_upload_file(filepath: str):
    """Delete uploaded file"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error deleting file: {e}")


def get_file_url(filepath: str) -> str:
    """Get file URL"""
    return f"/api/uploads/{os.path.basename(filepath)}"
