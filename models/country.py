#!/usr/bin/python3
"""
Country model module
"""

from models.base_model import BaseModel


class Country(BaseModel):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
