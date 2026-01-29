from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/postgres"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Files
    uploads_dir: str = "./uploads"
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS - list of allowed origins (as comma-separated string in env)
    allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    )
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse comma-separated origins string into list"""
        if isinstance(self.allowed_origins, str):
            return [origin.strip() for origin in self.allowed_origins.split(',') if origin.strip()]
        return self.allowed_origins if isinstance(self.allowed_origins, list) else []


@lru_cache()
def get_settings():
    return Settings()
