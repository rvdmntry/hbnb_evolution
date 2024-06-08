#!/usr/bin/python3
"""country"""


from model.base_model import BaseModel

class Country(BaseModel):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
