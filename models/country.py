import uuid
from datetime import datetime


class Country:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
