#!/usr/bin/python3

import json
import os
from models.user import User
from models.country import Country
from models.city import City
from models.amenity import Amenity
from models.place import Place
from datetime import datetime

class DataManager:
    def __init__(self, storage_file='data.json'):
        self.storage_file = storage_file
        self.storage = {
            "User": {},
            "Country": {},
            "City": {},
            "Amenity": {},
            "Place": {}
        }
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                data = json.load(file)
                for entity_type, entities in data.items():
                    for entity_id, entity_data in entities.items():
                        if entity_type == "User":
                            self.storage[entity_type][entity_id] = User(
                                email=entity_data.get('email'),
                                first_name=entity_data.get('first_name'),
                                last_name=entity_data.get('last_name')
                            )
                        elif entity_type == "Country":
                            self.storage[entity_type][entity_id] = Country(
                                code=entity_data.get('code'),
                                name=entity_data.get('name')
                            )
                        elif entity_type == "City":
                            self.storage[entity_type][entity_id] = City(
                                name=entity_data.get('name'),
                                country_code=entity_data.get('country_code')
                            )
                        elif entity_type == "Amenity":
                            self.storage[entity_type][entity_id] = Amenity(
                                name=entity_data.get('name')
                            )
                        elif entity_type == "Place":
                            self.storage[entity_type][entity_id] = Place(
                                name=entity_data.get('name'),
                                description=entity_data.get('description'),
                                address=entity_data.get('address'),
                                city_id=entity_data.get('city_id'),
                                latitude=entity_data.get('latitude'),
                                longitude=entity_data.get('longitude'),
                                host_id=entity_data.get('host_id'),
                                number_of_rooms=entity_data.get('number_of_rooms'),
                                number_of_bathrooms=entity_data.get('number_of_bathrooms'),
                                price_per_night=entity_data.get('price_per_night'),
                                max_guests=entity_data.get('max_guests'),
                                amenity_ids=entity_data.get('amenity_ids')
                            )

    def _save_data(self):
        data = {}
        for entity_type, entities in self.storage.items():
            data[entity_type] = {entity_id: entity.to_dict() for entity_id, entity in entities.items()}
        with open(self.storage_file, 'w') as file:
            json.dump(data, file, default=str, indent=4)

    def save(self, entity):
        entity_type = entity.__class__.__name__
        if entity_type == "Country":
            entity_id = entity.code  # Use 'code' as the identifier for Country
        else:
            entity_id = str(entity.id)
        self.storage[entity_type][entity_id] = entity
        self._save_data()

    def get(self, entity_id, entity_type):
        return self.storage[entity_type].get(entity_id)

    def get_all(self, entity_type):
        return list(self.storage[entity_type].values())

    def update(self, entity):
        entity_type = entity.__class__.__name__
        if entity_type == "Country":
            entity_id = entity.code  # Use 'code' as the identifier for Country
        else:
            entity_id = str(entity.id)
        self.storage[entity_type][entity_id] = entity
        self._save_data()

    def delete(self, entity_id, entity_type):
        if entity_id in self.storage[entity_type]:
            del self.storage[entity_type][entity_id]
            self._save_data()
            return True
        return False
