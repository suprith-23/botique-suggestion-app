from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_db, get_db_cursor
from app.schemas.upload import UploadListResponse
from app.utils.dependencies import get_admin_user
from app.services.upload_service import UploadService
from app.models.upload import ClothType, Occasion

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard/stats")
def get_dashboard_stats(
    db = Depends(get_db),
    current_admin = Depends(get_admin_user)
):
    """Get admin dashboard statistics"""
    
    total_uploads = UploadService.get_uploads_count(db)
    
    # Most popular cloth types
    with get_db_cursor(db) as cursor:
        cursor.execute(
            "SELECT cloth_type, COUNT(*) as count FROM uploads GROUP BY cloth_type ORDER BY count DESC"
        )
        cloth_stats = cursor.fetchall()
    
    # Most requested occasions
    with get_db_cursor(db) as cursor:
        cursor.execute(
            "SELECT occasion, COUNT(*) as count FROM uploads GROUP BY occasion ORDER BY count DESC"
        )
        occasion_stats = cursor.fetchall()
    
    return {
        "total_uploads": total_uploads,
        "cloth_types": [
            {"type": stat['cloth_type'], "count": stat['count']} for stat in cloth_stats
        ],
        "occasions": [
            {"occasion": stat['occasion'], "count": stat['count']} for stat in occasion_stats
        ]
    }


@router.get("/uploads", response_model=list[UploadListResponse])
def get_all_uploads(
    skip: int = 0,
    limit: int = 10,
    db = Depends(get_db),
    current_admin = Depends(get_admin_user)
):
    """Get all uploads (admin)"""
    uploads = UploadService.get_all_uploads(db, skip, limit)
    return [
        {
            "id": u.id,
            "cloth_type": u.cloth_type,
            "occasion": u.occasion,
            "created_at": u.created_at,
            "file_path": u.file_path
        } for u in uploads
    ]


@router.get("/uploads/by-type/{cloth_type}")
def get_uploads_by_type(
    cloth_type: str,
    db = Depends(get_db),
    current_admin = Depends(get_admin_user)
):
    """Get uploads by cloth type"""
    try:
        cloth_enum = ClothType(cloth_type)
        with get_db_cursor(db) as cursor:
            cursor.execute(
                "SELECT id, user_id, file_path, cloth_type, occasion, gender, age_group, budget_range, size_info, created_at FROM uploads WHERE cloth_type = %s",
                (cloth_type,)
            )
            results = cursor.fetchall()
        
        return [
            {
                "id": r['id'],
                "cloth_type": r['cloth_type'],
                "occasion": r['occasion'],
                "created_at": r['created_at'],
                "file_path": r['file_path']
            } for r in results
        ]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cloth type")


@router.get("/trending")
def get_trending_data(
    db = Depends(get_db),
    current_admin = Depends(get_admin_user)
):
    """Get trending colors, patterns, and designs"""
    
    # Most popular cloth types
    with get_db_cursor(db) as cursor:
        cursor.execute(
            "SELECT cloth_type, COUNT(*) as count FROM uploads GROUP BY cloth_type ORDER BY count DESC LIMIT 5"
        )
        top_cloths = cursor.fetchall()
    
    # Most popular occasions
    with get_db_cursor(db) as cursor:
        cursor.execute(
            "SELECT occasion, COUNT(*) as count FROM uploads GROUP BY occasion ORDER BY count DESC LIMIT 5"
        )
        top_occasions = cursor.fetchall()
    
    return {
        "trending_cloths": [
            {"cloth_type": cloth['cloth_type'], "count": cloth['count']} for cloth in top_cloths
        ],
        "trending_occasions": [
            {"occasion": occ['occasion'], "count": occ['count']} for occ in top_occasions
        ],
        "trending_colors": ["Gold", "Royal Blue", "Maroon", "Emerald Green", "Pink"],
        "trending_patterns": ["Zari", "Block Print", "Mirror Work", "Embroidery", "Geometric"]
    }
