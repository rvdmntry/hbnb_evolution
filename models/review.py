#!/usr/bin/python3
"""
Review model module
"""

from models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, user_id, place_id, rating, comment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
