from pydantic import BaseModel
from datetime import datetime


class DesignSuggestionBase(BaseModel):
    """Base design suggestion schema"""
    neck_design: str
    sleeve_style: str
    embroidery_pattern: str
    color_combination: str
    border_style: str
    description: str
    confidence_score: str = "High"


class DesignSuggestionCreate(DesignSuggestionBase):
    """Design suggestion creation schema"""
    pass


class DesignSuggestionResponse(DesignSuggestionBase):
    """Design suggestion response schema"""
    id: int
    upload_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SavedDesignResponse(BaseModel):
    """Saved design response schema"""
    id: int
    user_id: int
    design_suggestion_id: int
    saved_at: datetime
    
    class Config:
        from_attributes = True
