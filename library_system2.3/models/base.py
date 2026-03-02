"""
Base model with common functionality for all models
"""
from datetime import datetime
import uuid


class BaseModel:
    """Base class for all models with common attributes and methods"""
    
    def __init__(self, **kwargs):
        """Initialize base model with common fields"""
        self.id = kwargs.get('id', str(uuid.uuid4())[:8])
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create object from dictionary"""
        return cls(**data)
    
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"
    
    def __repr__(self):
        return self.__str__()