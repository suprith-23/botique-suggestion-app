from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_db
from app.schemas.design_suggestion import DesignSuggestionResponse, SavedDesignResponse
from app.services.upload_service import SavedDesignService, DesignSuggestionService
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/design-suggestions", tags=["Design Suggestions"])


@router.get("/{suggestion_id}", response_model=DesignSuggestionResponse)
def get_suggestion(
    suggestion_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get design suggestion by ID"""
    suggestion = DesignSuggestionService.get_suggestion_by_id(db, suggestion_id)
    
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    
    if suggestion.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return {
        "id": suggestion.id,
        "upload_id": suggestion.upload_id,
        "user_id": suggestion.user_id,
        "neck_design": suggestion.neck_design,
        "sleeve_style": suggestion.sleeve_style,
        "embroidery_pattern": suggestion.embroidery_pattern,
        "color_combination": suggestion.color_combination,
        "border_style": suggestion.border_style,
        "description": suggestion.description,
        "confidence_score": suggestion.confidence_score,
        "created_at": suggestion.created_at
    }


@router.post("/{suggestion_id}/save", response_model=SavedDesignResponse, status_code=status.HTTP_201_CREATED)
def save_design(
    suggestion_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Save a design suggestion"""
    try:
        saved = SavedDesignService.save_design(db, current_user.id, suggestion_id)
        if saved:
            return {
                "id": saved.id,
                "user_id": saved.user_id,
                "design_suggestion_id": saved.design_suggestion_id,
                "saved_at": saved.saved_at
            }
        raise ValueError("Failed to save design")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/saved/list", response_model=list[DesignSuggestionResponse])
def get_saved_designs(
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get user's saved designs"""
    saved_designs = SavedDesignService.get_user_saved_designs(db, current_user.id)
    
    # Get the actual design suggestions
    suggestions = []
    for saved in saved_designs:
        suggestion = DesignSuggestionService.get_suggestion_by_id(db, saved.design_suggestion_id)
        if suggestion:
            suggestions.append({
                "id": suggestion.id,
                "upload_id": suggestion.upload_id,
                "user_id": suggestion.user_id,
                "neck_design": suggestion.neck_design,
                "sleeve_style": suggestion.sleeve_style,
                "embroidery_pattern": suggestion.embroidery_pattern,
                "color_combination": suggestion.color_combination,
                "border_style": suggestion.border_style,
                "description": suggestion.description,
                "confidence_score": suggestion.confidence_score,
                "created_at": suggestion.created_at
            })
    
    return suggestions


@router.delete("/{saved_design_id}/save", status_code=status.HTTP_204_NO_CONTENT)
def unsave_design(
    saved_design_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Unsave a design suggestion"""
    SavedDesignService.unsave_design(db, saved_design_id)
