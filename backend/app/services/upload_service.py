from app.models.upload import Upload
from app.models.design_suggestion import DesignSuggestion
from app.models.saved_design import SavedDesign
from app.schemas.upload import UploadCreate
from app.models.user import User
from app.core.database import get_db_cursor


class UploadService:
    """Upload service"""
    
    @staticmethod
    def create_upload(conn, user_id: int, upload: UploadCreate, file_path: str) -> Upload:
        """Create new upload"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """INSERT INTO uploads (user_id, file_path, cloth_type, occasion, gender, age_group, budget_range, size_info)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                   RETURNING id, user_id, file_path, cloth_type, occasion, gender, age_group, budget_range, size_info, created_at""",
                (user_id, file_path, upload.cloth_type, upload.occasion, upload.gender, 
                 upload.age_group, upload.budget_range, getattr(upload, 'size_info', None))
            )
            result = cursor.fetchone()
            
            if result:
                return Upload(
                    id=result['id'],
                    user_id=result['user_id'],
                    file_path=result['file_path'],
                    cloth_type=result['cloth_type'],
                    occasion=result['occasion'],
                    gender=result['gender'],
                    age_group=result['age_group'],
                    budget_range=result['budget_range'],
                    size_info=result['size_info'],
                    created_at=result['created_at']
                )
        return None
    
    @staticmethod
    def get_upload_by_id(conn, upload_id: int) -> Upload:
        """Get upload by ID"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                "SELECT id, user_id, file_path, cloth_type, occasion, gender, age_group, budget_range, size_info, created_at FROM uploads WHERE id = %s",
                (upload_id,)
            )
            result = cursor.fetchone()
        
        if result:
            return Upload(
                id=result['id'],
                user_id=result['user_id'],
                file_path=result['file_path'],
                cloth_type=result['cloth_type'],
                occasion=result['occasion'],
                gender=result['gender'],
                age_group=result['age_group'],
                budget_range=result['budget_range'],
                size_info=result['size_info'],
                created_at=result['created_at']
            )
        return None
    
    @staticmethod
    def get_user_uploads(conn, user_id: int, skip: int = 0, limit: int = 10) -> list:
        """Get user uploads"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """SELECT id, user_id, file_path, cloth_type, occasion, gender, age_group, budget_range, size_info, created_at 
                   FROM uploads WHERE user_id = %s ORDER BY created_at DESC OFFSET %s LIMIT %s""",
                (user_id, skip, limit)
            )
            results = cursor.fetchall()
        
        return [Upload(
            id=r['id'],
            user_id=r['user_id'],
            file_path=r['file_path'],
            cloth_type=r['cloth_type'],
            occasion=r['occasion'],
            gender=r['gender'],
            age_group=r['age_group'],
            budget_range=r['budget_range'],
            size_info=r['size_info'],
            created_at=r['created_at']
        ) for r in results]
    
    @staticmethod
    def get_all_uploads(conn, skip: int = 0, limit: int = 10) -> list:
        """Get all uploads (admin)"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """SELECT id, user_id, file_path, cloth_type, occasion, gender, age_group, budget_range, size_info, created_at 
                   FROM uploads ORDER BY created_at DESC OFFSET %s LIMIT %s""",
                (skip, limit)
            )
            results = cursor.fetchall()
        
        return [Upload(
            id=r['id'],
            user_id=r['user_id'],
            file_path=r['file_path'],
            cloth_type=r['cloth_type'],
            occasion=r['occasion'],
            gender=r['gender'],
            age_group=r['age_group'],
            budget_range=r['budget_range'],
            size_info=r['size_info'],
            created_at=r['created_at']
        ) for r in results]
    
    @staticmethod
    def get_uploads_count(conn) -> int:
        """Get total uploads count"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM uploads")
            result = cursor.fetchone()
        
        return result['count'] if result else 0


class DesignSuggestionService:
    """Design suggestion service"""
    
    @staticmethod
    def create_suggestion(conn, upload_id: int, user_id: int, suggestion_data: dict) -> DesignSuggestion:
        """Create design suggestion"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """INSERT INTO design_suggestions 
                   (upload_id, user_id, neck_design, sleeve_style, embroidery_pattern, color_combination, border_style, description, confidence_score)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                   RETURNING id, upload_id, user_id, neck_design, sleeve_style, embroidery_pattern, color_combination, border_style, description, confidence_score, created_at""",
                (upload_id, user_id, suggestion_data['neck_design'], suggestion_data['sleeve_style'],
                 suggestion_data['embroidery_pattern'], suggestion_data['color_combination'],
                 suggestion_data['border_style'], suggestion_data['description'],
                 suggestion_data.get('confidence_score', 'High'))
            )
            result = cursor.fetchone()
            
            if result:
                return DesignSuggestion(
                    id=result['id'],
                    upload_id=result['upload_id'],
                    user_id=result['user_id'],
                    neck_design=result['neck_design'],
                    sleeve_style=result['sleeve_style'],
                    embroidery_pattern=result['embroidery_pattern'],
                    color_combination=result['color_combination'],
                    border_style=result['border_style'],
                    description=result['description'],
                    confidence_score=result['confidence_score'],
                    created_at=result['created_at']
                )
        return None
    
    @staticmethod
    def get_suggestion_by_id(conn, suggestion_id: int) -> DesignSuggestion:
        """Get suggestion by ID"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """SELECT id, upload_id, user_id, neck_design, sleeve_style, embroidery_pattern, color_combination, border_style, description, confidence_score, created_at 
                   FROM design_suggestions WHERE id = %s""",
                (suggestion_id,)
            )
            result = cursor.fetchone()
        
        if result:
            return DesignSuggestion(
                id=result['id'],
                upload_id=result['upload_id'],
                user_id=result['user_id'],
                neck_design=result['neck_design'],
                sleeve_style=result['sleeve_style'],
                embroidery_pattern=result['embroidery_pattern'],
                color_combination=result['color_combination'],
                border_style=result['border_style'],
                description=result['description'],
                confidence_score=result['confidence_score'],
                created_at=result['created_at']
            )
        return None
    
    @staticmethod
    def get_upload_suggestions(conn, upload_id: int) -> list:
        """Get suggestions for an upload"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """SELECT id, upload_id, user_id, neck_design, sleeve_style, embroidery_pattern, color_combination, border_style, description, confidence_score, created_at 
                   FROM design_suggestions WHERE upload_id = %s""",
                (upload_id,)
            )
            results = cursor.fetchall()
        
        return [DesignSuggestion(
            id=r['id'],
            upload_id=r['upload_id'],
            user_id=r['user_id'],
            neck_design=r['neck_design'],
            sleeve_style=r['sleeve_style'],
            embroidery_pattern=r['embroidery_pattern'],
            color_combination=r['color_combination'],
            border_style=r['border_style'],
            description=r['description'],
            confidence_score=r['confidence_score'],
            created_at=r['created_at']
        ) for r in results]
    
    @staticmethod
    def get_user_suggestions(conn, user_id: int, skip: int = 0, limit: int = 10) -> list:
        """Get user suggestions"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """SELECT id, upload_id, user_id, neck_design, sleeve_style, embroidery_pattern, color_combination, border_style, description, confidence_score, created_at 
                   FROM design_suggestions WHERE user_id = %s ORDER BY created_at DESC OFFSET %s LIMIT %s""",
                (user_id, skip, limit)
            )
            results = cursor.fetchall()
        
        return [DesignSuggestion(
            id=r['id'],
            upload_id=r['upload_id'],
            user_id=r['user_id'],
            neck_design=r['neck_design'],
            sleeve_style=r['sleeve_style'],
            embroidery_pattern=r['embroidery_pattern'],
            color_combination=r['color_combination'],
            border_style=r['border_style'],
            description=r['description'],
            confidence_score=r['confidence_score'],
            created_at=r['created_at']
        ) for r in results]


class SavedDesignService:
    """Saved design service"""
    
    @staticmethod
    def save_design(conn, user_id: int, design_suggestion_id: int) -> SavedDesign:
        """Save a design"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """INSERT INTO saved_designs (user_id, design_suggestion_id)
                   VALUES (%s, %s)
                   RETURNING id, user_id, design_suggestion_id, saved_at""",
                (user_id, design_suggestion_id)
            )
            result = cursor.fetchone()
            
            if result:
                return SavedDesign(
                    id=result['id'],
                    user_id=result['user_id'],
                    design_suggestion_id=result['design_suggestion_id'],
                    saved_at=result['saved_at']
                )
        return None
    
    @staticmethod
    def get_user_saved_designs(conn, user_id: int) -> list:
        """Get user's saved designs"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """SELECT id, user_id, design_suggestion_id, saved_at 
                   FROM saved_designs WHERE user_id = %s ORDER BY saved_at DESC""",
                (user_id,)
            )
            results = cursor.fetchall()
        
        return [SavedDesign(
            id=r['id'],
            user_id=r['user_id'],
            design_suggestion_id=r['design_suggestion_id'],
            saved_at=r['saved_at']
        ) for r in results]
    
    @staticmethod
    def unsave_design(conn, saved_design_id: int) -> bool:
        """Unsave a design"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute("DELETE FROM saved_designs WHERE id = %s", (saved_design_id,))
        
        return True
