#!/usr/bin/python3

from datetime import datetime
import uuid

class Amenity:
    def __init__(self, name):
        self.id = uuid.uuid4().hex
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, name=None):
        if name:
            self.name = name
            self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
