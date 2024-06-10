import uuid
from datetime import datetime
from models.user import User


class Place:
    def __init__(self, name, description, address, city, latitude, longitude, host, number_of_rooms, bathrooms, price_per_night, max_guests, amenities=None, reviews=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.address = address
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.host = host
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = amenities if amenities is not None else []
        self.reviews = reviews if reviews is not None else []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "host": self.host.to_dict() if self.host else None,
            "number_of_rooms": self.number_of_rooms,
            "bathrooms": self.bathrooms,
            "price_per_night": self.price_per_night,
            "max_guests": self.max_guests,
            "amenities": [amenity.to_dict() for amenity in self.amenities],
            "reviews": [review.to_dict() for review in self.reviews],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
