#!/usr/bin/python3
from .base_model.py import BaseModel


class User(BaseModel):
    def __init__(self, email, password, first_name, last_name):
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
        })
        return user_dict

    def save(self):
        super().save()
        # Implement file-based persistence, e.g., saving to a JSON file
