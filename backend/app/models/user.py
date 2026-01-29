from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    USER = "user"


class User:
    """User model"""
    
    def __init__(self, id=None, email=None, username=None, hashed_password=None, 
                 role=UserRole.USER, full_name=None, is_active=True, 
                 created_at=None, updated_at=None):
        self.id = id
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.role = role
        self.full_name = full_name
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
