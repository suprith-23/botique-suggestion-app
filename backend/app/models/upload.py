from datetime import datetime
import enum


class ClothType(str, enum.Enum):
    """Cloth types"""
    SAREE = "saree"
    KURTI = "kurti"
    LEHENGA = "lehenga"
    SHIRT = "shirt"
    DRESS = "dress"
    BLOUSE = "blouse"
    DUPATTA = "dupatta"
    SHAWL = "shawl"


class Occasion(str, enum.Enum):
    """Occasion types"""
    WEDDING = "wedding"
    CASUAL = "casual"
    FESTIVAL = "festival"
    PARTY = "party"
    OFFICE = "office"


class Gender(str, enum.Enum):
    """Gender"""
    MALE = "male"
    FEMALE = "female"
    UNISEX = "unisex"


class AgeGroup(str, enum.Enum):
    """Age group"""
    CHILD = "child"
    ADULT = "adult"
    SENIOR = "senior"


class BudgetRange(str, enum.Enum):
    """Budget range"""
    LOW = "1000-3000"  # Simple prints
    MEDIUM = "3000-8000"  # Medium embroidery
    HIGH = "10000+"  # Premium heavy designs


class Upload:
    """Upload model"""
    
    def __init__(self, id=None, user_id=None, file_path=None, cloth_type=None,
                 occasion=None, gender=None, age_group=None, budget_range=None,
                 size_info=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.file_path = file_path
        self.cloth_type = cloth_type
        self.occasion = occasion
        self.gender = gender
        self.age_group = age_group
        self.budget_range = budget_range
        self.size_info = size_info
        self.created_at = created_at or datetime.utcnow()
    
    def __repr__(self):
        return f"<Upload(id={self.id}, user_id={self.user_id})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'file_path': self.file_path,
            'cloth_type': self.cloth_type,
            'occasion': self.occasion,
            'gender': self.gender,
            'age_group': self.age_group,
            'budget_range': self.budget_range,
            'size_info': self.size_info,
            'created_at': self.created_at
        }
    
    def __repr__(self):
        return f"<Upload(id={self.id}, user_id={self.user_id})>"
