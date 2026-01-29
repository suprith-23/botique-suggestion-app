from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, status
from app.core.database import get_db
from app.schemas.upload import UploadCreate, UploadResponse, UploadListResponse
from app.schemas.design_suggestion import DesignSuggestionResponse
from app.services.upload_service import UploadService, DesignSuggestionService
from app.services.design_suggestion_service import DesignSuggestionEngine
from app.utils.file_handler import save_upload_file, get_file_url
from app.utils.dependencies import get_current_user
from app.models.upload import ClothType, Occasion, Gender, AgeGroup, BudgetRange

router = APIRouter(prefix="/api/uploads", tags=["Uploads"])


@router.post("", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def create_upload(
    file: UploadFile = File(...),
    cloth_type: ClothType = Form(...),
    occasion: Occasion = Form(...),
    gender: Gender = Form(...),
    age_group: AgeGroup = Form(...),
    budget_range: BudgetRange = Form(...),
    fabric_description: str = Form(None),
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Upload cloth image and create upload record"""
    
    # Save file
    filepath = await save_upload_file(file, current_user.id)
    
    # Create upload
    upload_data = UploadCreate(
        cloth_type=cloth_type.value if hasattr(cloth_type, 'value') else cloth_type,
        occasion=occasion.value if hasattr(occasion, 'value') else occasion,
        gender=gender.value if hasattr(gender, 'value') else gender,
        age_group=age_group.value if hasattr(age_group, 'value') else age_group,
        budget_range=budget_range.value if hasattr(budget_range, 'value') else budget_range,
        size_info=fabric_description
    )
    
    db_upload = UploadService.create_upload(db, current_user.id, upload_data, filepath)
    
    # Generate design suggestions
    suggestions = DesignSuggestionEngine.generate_suggestions(db_upload)
    DesignSuggestionService.create_suggestion(db, db_upload.id, current_user.id, suggestions)
    
    return {
        "id": db_upload.id,
        "user_id": db_upload.user_id,
        "file_path": db_upload.file_path,
        "cloth_type": db_upload.cloth_type,
        "occasion": db_upload.occasion,
        "gender": db_upload.gender,
        "age_group": db_upload.age_group,
        "budget_range": db_upload.budget_range,
        "size_info": db_upload.size_info,
        "created_at": db_upload.created_at
    }


@router.get("/my-uploads", response_model=list[UploadListResponse])
def get_my_uploads(
    skip: int = 0,
    limit: int = 10,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get user's uploads"""
    uploads = UploadService.get_user_uploads(db, current_user.id, skip, limit)
    return [
        {
            "id": u.id,
            "cloth_type": u.cloth_type,
            "occasion": u.occasion,
            "created_at": u.created_at,
            "file_path": u.file_path
        } for u in uploads
    ]


@router.get("/{upload_id}", response_model=UploadResponse)
def get_upload(
    upload_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get upload by ID"""
    upload = UploadService.get_upload_by_id(db, upload_id)
    
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    if upload.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return {
        "id": upload.id,
        "user_id": upload.user_id,
        "file_path": upload.file_path,
        "cloth_type": upload.cloth_type,
        "occasion": upload.occasion,
        "gender": upload.gender,
        "age_group": upload.age_group,
        "budget_range": upload.budget_range,
        "size_info": upload.size_info,
        "created_at": upload.created_at
    }


@router.get("/{upload_id}/suggestions", response_model=list[DesignSuggestionResponse])
def get_upload_suggestions(
    upload_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get design suggestions for an upload"""
    upload = UploadService.get_upload_by_id(db, upload_id)
    
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    if upload.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    suggestions = DesignSuggestionService.get_upload_suggestions(db, upload_id)
    return [
        {
            "id": s.id,
            "upload_id": s.upload_id,
            "user_id": s.user_id,
            "neck_design": s.neck_design,
            "sleeve_style": s.sleeve_style,
            "embroidery_pattern": s.embroidery_pattern,
            "color_combination": s.color_combination,
            "border_style": s.border_style,
            "description": s.description,
            "confidence_score": s.confidence_score,
            "created_at": s.created_at
        } for s in suggestions
    ]
