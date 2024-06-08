#!/usr/bin/python3
"""class Data Manager development"""


import json
import os
from persistence.ipersistence_manager import IPersistenceManager

class DataManager(IPersistenceManager):
    __file_path = "data.json"
    __objects = {}

    def __init__(self):
        self.load()

    def save(self, entity):
        """Save to the storage"""
        entity_dict = entity.to_dict()
        DataManager.__objects[entity_dict['id']] = entity_dict
        self._save_to_file()

    def get(self, entity_id, entity_type):
        """Retrieve an entity based on ID and type"""
        entity_dict = DataManager.__objects.get(entity_id)
        if entity_dict and entity_dict['type'] == entity_type:
            return entity_dict
        return None

    def update(self, entity):
        """Update an entity in the storage"""
        entity_dict = entity.to_dict()
        if entity_dict['id'] in DataManager.__objects:
            DataManager.__objects[entity_dict['id']] = entity_dict
            self._save_to_file()

    def delete(self, entity_id, entity_type):
        """Delete an entity from the storage"""
        entity_dict = DataManager.__objects.get(entity_id)
        if entity_dict and entity_dict['type'] == entity_type:
            del DataManager.__objects[entity_id]
            self._save_to_file()

    def _save_to_file(self):
        """Save the objects to a file"""
        with open(DataManager.__file_path, 'w') as file:
            json.dump(DataManager.__objects, file)

    def load(self):
        """Load the objects from a file"""
        if os.path.exists(DataManager.__file_path):
            with open(DataManager.__file_path, 'r') as file:
                DataManager.__objects = json.load(file)
