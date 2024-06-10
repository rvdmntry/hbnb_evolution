import json
import os
from uuid import uuid4
from datetime import datetime
from models.user import User
from models.place import Place
from models.city import City
from models.country import Country
from models.review import Review
from models.amenity import Amenity
from persistence.i_persistence_manager import IPersistenceManager


class DataManager(IPersistenceManager):
    __file_path = "data.json"
    __objects = {}

    def __init__(self):
        self.reload()

    def save(self, entity):
        entity_id = entity.id
        entity_type = entity.__class__.__name__
        key = f"{entity_type}.{entity_id}"
        self.__objects[key] = entity
        self.__save_to_file()

    def get(self, entity_id, entity_type):
        key = f"{entity_type}.{entity_id}"
        return self.__objects.get(key, None)

    def update(self, entity):
        entity_id = entity.id
        entity_type = entity.__class__.__name__
        key = f"{entity_type}.{entity_id}"
        if key in self.__objects:
            self.__objects[key] = entity
            self.__save_to_file()

    def delete(self, entity_id, entity_type):
        key = f"{entity_type}.{entity_id}"
        if key in self.__objects:
            del self.__objects[key]
            self.__save_to_file()

    def __save_to_file(self):
        with open(self.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as f:
                self.__objects = json.load(f)
                for key, value in self.__objects.items():
                    entity_type, entity_id = key.split('.')
                    if entity_type == 'User':
                        self.__objects[key] = User(**value)
                    elif entity_type == 'Place':
                        self.__objects[key] = Place(**value)
                    elif entity_type == 'City':
                        self.__objects[key] = City(**value)
                    elif entity_type == 'Country':
                        self.__objects[key] = Country(**value)
                    elif entity_type == 'Review':
                        self.__objects[key] = Review(**value)
                    elif entity_type == 'Amenity':
                        self.__objects[key] = Amenity(**value)
