from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import get_settings
from app.core.database import init_db
from app.routes import auth, upload, design_suggestion, admin
import os
import uvicorn

settings = get_settings()

# Initialize database tables
try:
    init_db()
except Exception as e:
    print(f"Database initialization error: {e}")

# Create FastAPI app
app = FastAPI(
    title="Boutique Suggestion API",
    description="AI-powered boutique design suggestion system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(design_suggestion.router)
app.include_router(admin.router)

# Static files for uploads
os.makedirs(settings.uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.uploads_dir), name="uploads")


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Boutique Suggestion API",
        "version": "1.0.0",
        "docs": "/docs"
    }



@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
