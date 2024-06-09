from flask import Blueprint, request, jsonify
from models.data_manager import DataManager
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.user import User

places_blueprint = Blueprint('places', __name__)
data_manager = DataManager()

# Validation functions


def validate_place_payload(data):
    required_fields = ["name", "description", "address", "city_id", "latitude", "longitude", "host_id",
                       "number_of_rooms", "number_of_bathrooms", "price_per_night", "max_guests", "amenity_ids"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    if not isinstance(data["latitude"], (float, int)) or not (-90 <= data["latitude"] <= 90):
        return False, "Invalid latitude value"
    if not isinstance(data["longitude"], (float, int)) or not (-180 <= data["longitude"] <= 180):
        return False, "Invalid longitude value"
    if not isinstance(data["number_of_rooms"], int) or data["number_of_rooms"] < 0:
        return False, "Invalid number of rooms"
    if not isinstance(data["number_of_bathrooms"], int) or data["number_of_bathrooms"] < 0:
        return False, "Invalid number of bathrooms"
    if not isinstance(data["max_guests"], int) or data["max_guests"] < 0:
        return False, "Invalid max guests"
    if not isinstance(data["price_per_night"], (float, int)) or data["price_per_night"] < 0:
        return False, "Invalid price per night"

    if not data_manager.get(data["city_id"], City):
        return False, "City ID does not exist"
    if not data_manager.get(data["host_id"], User):
        return False, "Host ID does not exist"

    for amenity_id in data["amenity_ids"]:
        if not data_manager.get(amenity_id, Amenity):
            return False, f"Amenity ID {amenity_id} does not exist"

    return True, ""

# POST /places: Create a new place


@places_blueprint.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()
    is_valid, message = validate_place_payload(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    place = Place(**data)
    data_manager.save(place)
    return jsonify(place.to_dict()), 201

# GET /places: Retrieve a list of all places


@places_blueprint.route('/places', methods=['GET'])
def get_places():
    places = [place.to_dict() for place in data_manager.get_all(Place)]
    return jsonify(places), 200

# GET /places/<place_id>: Retrieve detailed information about a specific place


@places_blueprint.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, Place)
    if place:
        place_data = place.to_dict()
        city = data_manager.get(place.city_id, City)
        if city:
            place_data["city"] = city.to_dict()
        amenities = [data_manager.get(amenity_id, Amenity).to_dict()
                     for amenity_id in place.amenity_ids]
        place_data["amenities"] = amenities
        return jsonify(place_data), 200
    return jsonify({"error": "Place not found"}), 404

# PUT /places/<place_id>: Update an existing place’s information


@places_blueprint.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = data_manager.get(place_id, Place)
    if not place:
        return jsonify({"error": "Place not found"}), 404

    data = request.get_json()
    is_valid, message = validate_place_payload(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    place.update(**data)
    data_manager.update(place)
    return jsonify(place.to_dict()), 200

# DELETE /places/<place_id>: Delete a specific place


@places_blueprint.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, Place)
    if not place:
        return jsonify({"error": "Place not found"}), 404

    data_manager.delete(place_id, Place)
    return '', 204
