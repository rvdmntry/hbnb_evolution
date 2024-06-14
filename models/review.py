#!/usr/bin/python3


from datetime import datetime
import uuid

class Review:
    def __init__(self, place_id, user_id, rating, comment):
        self.id = uuid.uuid4()
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
