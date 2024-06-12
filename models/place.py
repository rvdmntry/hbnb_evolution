#!/usr/bin/python3
from models.base_model.py import BaseModel


class Place(BaseModel):
    def __init__(self, name, description, address, city_id, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests, latitude=None, longitude=None):
        super().__init__()
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.latitude = latitude
        self.longitude = longitude
        self.amenities = []
        self.reviews = []

    def to_dict(self):
        place_dict = super().to_dict()
        place_dict.update({
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city_id': str(self.city_id),
            'host_id': str(self.host_id),
            'number_of_rooms': self.number_of_rooms,
            'number_of_bathrooms': self.number_of_bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'reviews': [review.to_dict() for review in self.reviews],
        })
        return place_dict

    def save(self):
        super().save()
        # Implement file-based persistence
