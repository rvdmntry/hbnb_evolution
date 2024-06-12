#!/usr/bin/python3
import json
import os
from .ipersistence_manager import IPersistenceManager


class DataManager(IPersistenceManager):

    def __init__(self, storage_dir='data'):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self._load_countries()

    def _load_countries(self):
        with open(os.path.join(self.storage_dir, 'countries.json'), 'r') as file:
            self.countries = json.load(file)

    def save(self, entity):
        entity_type = type(entity).__name__.lower()
        entity_dict = entity.to_dict()
        entity_id = entity_dict['id']
        filepath = os.path.join(
            self.storage_dir, f"{entity_type}s/{entity_id}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            json.dump(entity_dict, file)

    def get(self, entity_id, entity_type):
        entity_type = entity_type.lower()
        filepath = os.path.join(
            self.storage_dir, f"{entity_type}s/{entity_id}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r') as file:
            entity_dict = json.load(file)
        return entity_dict

    def update(self, entity):
        # For file-based storage, save and update are the same
        self.save(entity)

    def delete(self, entity_id, entity_type):
        entity_type = entity_type.lower()
        filepath = os.path.join(
            self.storage_dir, f"{entity_type}s/{entity_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)

    def get_all_countries(self):
        return self.countries

    def get_country(self, country_code):
        for country in self.countries:
            if country['code'] == country_code:
                return country
        return None
