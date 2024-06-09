# models/data_manager.py

import json
import os
from models.ipersistence_manager import IPersistenceManager


import json
import os


class DataManager(IPersistenceManager):
    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        self.reload()

    def save(self, entity):
        self.__objects[entity.id] = entity
        self.save_to_file()

    def get(self, entity_id, entity_type):
        return self.__objects.get(entity_id)

    def update(self, entity):
        if entity.id in self.__objects:
            self.__objects[entity.id] = entity
            self.save_to_file()

    def delete(self, entity_id, entity_type):
        if entity_id in self.__objects:
            del self.__objects[entity_id]
            self.save_to_file()

    def save_to_file(self):
        with open(self.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as f:
                objects = json.load(f)
                for obj_id, obj_data in objects.items():
                    class_name = obj_data.get('__class__')
                    if class_name:
                        cls = globals().get(class_name)
                        if cls:
                            self.__objects[obj_id] = cls(**obj_data)
