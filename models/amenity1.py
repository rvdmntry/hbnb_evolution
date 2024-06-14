#!/usr/bin/python3
import os
import json
from .base_model import BaseModel
from .data_manager import DataManager

data_manager = DataManager()


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict

    def save(self):
        data_manager.save(self)

    @staticmethod
    def get(amenity_id):
        amenity_dict = data_manager.get(amenity_id, 'amenity')
        if amenity_dict:
            amenity = Amenity(name=amenity_dict['name'])
            amenity.id = amenity_dict['id']
            amenity.created_at = amenity_dict['created_at']
            amenity.updated_at = amenity_dict['updated_at']
            return amenity
        return None

    @staticmethod
    def get_all():
        amenities = []
        amenity_files = os.listdir('data/amenities')
        for amenity_file in amenity_files:
            with open(os.path.join('data/amenities', amenity_file), 'r') as file:
                amenity_dict = json.load(file)
                amenity = Amenity(name=amenity_dict['name'])
                amenity.id = amenity_dict['id']
                amenity.created_at = amenity_dict['created_at']
                amenity.updated_at = amenity_dict['updated_at']
                amenities.append(amenity)
        return amenities

    @staticmethod
    def delete(amenity_id):
        data_manager.delete(amenity_id, 'amenity')
