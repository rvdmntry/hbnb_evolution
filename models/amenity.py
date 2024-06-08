#!/usr/bin/python3
"""amenities"""


from model.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
