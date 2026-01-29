from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.upload import ClothType, Occasion, Gender, AgeGroup, BudgetRange


class UploadBase(BaseModel):
    """Base upload schema"""
    cloth_type: ClothType
    occasion: Occasion
    gender: Gender
    age_group: AgeGroup
    budget_range: BudgetRange
    fabric_description: Optional[str] = None


class UploadCreate(UploadBase):
    """Upload creation schema"""
    pass


class UploadResponse(UploadBase):
    """Upload response schema"""
    id: int
    user_id: int
    file_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UploadListResponse(BaseModel):
    """Upload list response schema"""
    id: int
    cloth_type: ClothType
    occasion: Occasion
    file_path: str
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True
