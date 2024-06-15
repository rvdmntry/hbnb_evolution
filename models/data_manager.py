#!/usr/bin/python3

import json
import os
from models.ipersistence_manager import IPersistenceManager
from datetime import datetime

class DataManager(IPersistenceManager):
    def __init__(self, storage_file='data.json'):
        self.storage_file = storage_file

    def _load_data(self):
        if not os.path.exists(self.storage_file):
            return {}
        with open(self.storage_file, 'r') as file:
            data = json.load(file)
            # Deserialize datetime fields
            for entity_type in data:
                for entity_id in data[entity_type]:
                    entity = data[entity_type][entity_id]
                    if 'created_at' in entity:
                        entity['created_at'] = datetime.fromisoformat(entity['created_at'])
                    if 'updated_at' in entity:
                        entity['updated_at'] = datetime.fromisoformat(entity['updated_at'])
            return data

    def _save_data(self, data):
        # Serialize datetime fields
        for entity_type in data:
            for entity_id in data[entity_type]:
                entity = data[entity_type][entity_id]
                if 'created_at' in entity:
                    entity['created_at'] = entity['created_at'].isoformat()
                if 'updated_at' in entity:
                    entity['updated_at'] = entity['updated_at'].isoformat()
        with open(self.storage_file, 'w') as file:
            json.dump(data, file, indent=4)  # Added indent for readability

    def save(self, entity):
        data = self._load_data()
        entity_type = entity.__class__.__name__
        if entity_type not in data:
            data[entity_type] = {}
        data[entity_type][entity.id] = entity.to_dict()
        self._save_data(data)

    def get(self, entity_id, entity_type):
        data = self._load_data()
        if entity_type in data and entity_id in data[entity_type]:
            entity_dict = data[entity_type][entity_id]
            entity_class = globals()[entity_type]
            return entity_class(**entity_dict)
        return None

    def update(self, entity):
        self.save(entity)  # Save handles both create and update

    def delete(self, entity_id, entity_type):
        data = self._load_data()
        if entity_type in data and entity_id in data[entity_type]:
            del data[entity_type][entity_id]
            self._save_data(data)

    def get_all(self, entity_type):
        data = self._load_data()
        entity_class = globals().get(entity_type)
        if entity_class:
            return [entity_class(**item) for item in data.get(entity_type, {}).values()]
        return []
