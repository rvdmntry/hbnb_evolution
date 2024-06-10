import json
import os


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    @classmethod
    def all(cls):
        return cls.__objects

    @classmethod
    def save(cls):
        with open(cls.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in cls.__objects.items()}, f)

    @classmethod
    def reload(cls):
        if os.path.exists(cls.__file_path):
            with open(cls.__file_path, 'r') as f:
                cls.__objects = json.load(f)

    @classmethod
    def new(cls, obj):
        cls.__objects[obj.__class__.__name__ + '.' + obj.id] = obj

    @classmethod
    def delete(cls, obj):
        key = obj.__class__.__name__ + '.' + obj.id
        if key in cls.__objects:
            del cls.__objects[key]
