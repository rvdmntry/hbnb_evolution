#!/usr/bin/python3
"""
Base model module
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    A base class for all models in our HBnB clone
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new model
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)

    def save(self):
        """
        Update `updated_at` with current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Return a dictionary containing all keys/values of the instance
        """
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = self.__class__.__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary
