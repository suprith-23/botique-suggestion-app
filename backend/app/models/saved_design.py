from datetime import datetime


class SavedDesign:
    """Saved Design model"""
    
    def __init__(self, id=None, user_id=None, design_suggestion_id=None, saved_at=None):
        self.id = id
        self.user_id = user_id
        self.design_suggestion_id = design_suggestion_id
        self.saved_at = saved_at or datetime.utcnow()
    
    def __repr__(self):
        return f"<SavedDesign(id={self.id}, user_id={self.user_id}, design_suggestion_id={self.design_suggestion_id})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'design_suggestion_id': self.design_suggestion_id,
            'saved_at': self.saved_at
        }
