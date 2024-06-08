#!/usr/bin/python3
"""
File Storage module
"""

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
