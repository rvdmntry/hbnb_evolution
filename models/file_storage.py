#!/usr/bin/python3
"""
User model module
"""

from models.base_model import BaseModel
from models.file_storage import FileStorage


class User(BaseModel):
    users = {}

    def __init__(self, email, password, first_name='', last_name='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if email in User.users:
            raise ValueError("Email already exists")
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        User.users[email] = self
        FileStorage.save(self)
