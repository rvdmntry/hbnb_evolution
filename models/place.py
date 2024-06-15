#!/usr/bin/python3

from datetime import datetime
import uuid

class Place:
    def __init__(self, name, description, address, city_id, latitude, longitude, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests, amenity_ids):
        self.id = uuid.uuid4().hex
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenity_ids = amenity_ids
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, name=None, description=None, address=None, city_id=None, latitude=None, longitude=None, host_id=None, number_of_rooms=None, number_of_bathrooms=None, price_per_night=None, max_guests=None, amenity_ids=None):
        if name:
            self.name = name
        if description:
            self.description = description
        if address:
            self.address = address
        if city_id:
            self.city_id = city_id
        if latitude:
            self.latitude = latitude
        if longitude:
            self.longitude = longitude
        if host_id:
            self.host_id = host_id
        if number_of_rooms:
            self.number_of_rooms = number_of_rooms
        if number_of_bathrooms:
            self.number_of_bathrooms = number_of_bathrooms
        if price_per_night:
            self.price_per_night = price_per_night
        if max_guests:
            self.max_guests = max_guests
        if amenity_ids is not None:
            self.amenity_ids = amenity_ids
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city_id': self.city_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'host_id': self.host_id,
            'number_of_rooms': self.number_of_rooms,
            'number_of_bathrooms': self.number_of_bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenity_ids': self.amenity_ids,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
