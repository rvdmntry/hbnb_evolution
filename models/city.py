import uuid
from datetime import datetime


class City:
    def __init__(self, name, country):
        self.id = str(uuid.uuid4())
        self.name = name
        self.country = country
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country.to_dict() if self.country else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
