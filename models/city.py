# models/city.py

import uuid
from datetime import datetime


class City:
    def __init__(self, name, country_code):
        self.id = str(uuid.uuid4())
        self.name = name
        self.country_code = country_code
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country_code': self.country_code,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
