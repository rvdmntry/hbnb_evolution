#!/usr/bin/python3
"""file storage"""


import json
import os

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    @classmethod
    def save(cls, obj):
        cls.__objects[obj.id] = obj.to_dict()
        with open(cls.__file_path, 'w') as f:
            json.dump(cls.__objects, f)

    @classmethod
    def load(cls):
        if os.path.exists(cls.__file_path):
            with open(cls.__file_path, 'r') as f:
                cls.__objects = json.load(f)

    @classmethod
    def get(cls, obj_id):
        return cls.__objects.get(obj_id)

from persistence.file_storage import FileStorage

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
