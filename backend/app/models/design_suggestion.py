from datetime import datetime


class DesignSuggestion:
    """Design Suggestion model"""
    
    def __init__(self, id=None, upload_id=None, user_id=None, neck_design=None,
                 sleeve_style=None, embroidery_pattern=None, color_combination=None,
                 border_style=None, description=None, confidence_score="High",
                 created_at=None):
        self.id = id
        self.upload_id = upload_id
        self.user_id = user_id
        self.neck_design = neck_design
        self.sleeve_style = sleeve_style
        self.embroidery_pattern = embroidery_pattern
        self.color_combination = color_combination
        self.border_style = border_style
        self.description = description
        self.confidence_score = confidence_score
        self.created_at = created_at or datetime.utcnow()
    
    def __repr__(self):
        return f"<DesignSuggestion(id={self.id}, upload_id={self.upload_id})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'upload_id': self.upload_id,
            'user_id': self.user_id,
            'neck_design': self.neck_design,
            'sleeve_style': self.sleeve_style,
            'embroidery_pattern': self.embroidery_pattern,
            'color_combination': self.color_combination,
            'border_style': self.border_style,
            'description': self.description,
            'confidence_score': self.confidence_score,
            'created_at': self.created_at
        }
