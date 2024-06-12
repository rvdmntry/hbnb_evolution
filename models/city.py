#!/usr/bin/python3
import os
import json
from .base_model import BaseModel
from .data_manager import DataManager

data_manager = DataManager()


class City(BaseModel):
    def __init__(self, name, country_code):
        super().__init__()
        self.name = name
        self.country_code = country_code

    def to_dict(self):
        city_dict = super().to_dict()
        city_dict.update({
            'name': self.name,
            'country_code': self.country_code
        })
        return city_dict

    def save(self):
        data_manager.save(self)

    @staticmethod
    def get(city_id):
        city_dict = data_manager.get(city_id, 'city')
        if city_dict:
            city = City(
                name=city_dict['name'],
                country_code=city_dict['country_code']
            )
            city.id = city_dict['id']
            city.created_at = city_dict['created_at']
            city.updated_at = city_dict['updated_at']
            return city
        return None

    @staticmethod
    def get_all():
        cities = []
        city_files = os.listdir('data/cities')
        for city_file in city_files:
            with open(os.path.join('data/cities', city_file), 'r') as file:
                city_dict = json.load(file)
                city = City(
                    name=city_dict['name'],
                    country_code=city_dict['country_code']
                )
                city.id = city_dict['id']
                city.created_at = city_dict['created_at']
                city.updated_at = city_dict['updated_at']
                cities.append(city)
        return cities

    @staticmethod
    def delete(city_id):
        data_manager.delete(city_id, 'city')
