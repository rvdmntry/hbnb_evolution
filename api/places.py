#!/usr/bin/python3


from flask import Flask, request, jsonify, make_response
from models.place import Place
from persistence.data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()

@app.route('/places', methods=['POST'])
def create_place():
    data = request.json
    required_fields = ["name", "description", "address", "city_id", "latitude", "longitude", "host_id", "number_of_rooms", "number_of_bathrooms", "price_per_night", "max_guests", "amenity_ids"]
    if not all(field in data for field in required_fields):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    if not isinstance(data["amenity_ids"], list):
        return make_response(jsonify({"error": "amenity_ids should be a list"}), 400)

    # Validate geographical coordinates
    if not (-90 <= data["latitude"] <= 90) or not (-180 <= data["longitude"] <= 180):
        return make_response(jsonify({"error": "Invalid geographical coordinates"}), 400)

    # Validate non-negative integers
    if any(data[field] < 0 for field in ["number_of_rooms", "number_of_bathrooms", "max_guests"]):
        return make_response(jsonify({"error": "Room, bathroom, and guest capacities must be non-negative integers"}), 400)

    # Validate price per night
    if data["price_per_night"] < 0:
        return make_response(jsonify({"error": "Price per night must be a positive value"}), 400)

    # Validate city_id
    if data_manager.get(data["city_id"], "City") is None:
        return make_response(jsonify({"error": "City not found"}), 404)

    # Validate amenity_ids
    for amenity_id in data["amenity_ids"]:
        if data_manager.get(amenity_id, "Amenity") is None:
            return make_response(jsonify({"error": f"Amenity {amenity_id} not found"}), 404)

    place = Place(
        name=data["name"],
        description=data["description"],
        address=data["address"],
        city_id=data["city_id"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        host_id=data["host_id"],
        number_of_rooms=data["number_of_rooms"],
        number_of_bathrooms=data["number_of_bathrooms"],
        price_per_night=data["price_per_night"],
        max_guests=data["max_guests"],
        amenity_ids=data["amenity_ids"]
    )
    data_manager.save(place)
    return make_response(jsonify(place.__dict__), 201)

@app.route('/places', methods=['GET'])
def get_places():
    places = list(data_manager.storage["Place"].values())
    return jsonify([place.__dict__ for place in places])

@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, "Place")
    if place is None:
        return make_response(jsonify({"error": "Place not found"}), 404)
    return jsonify(place.__dict__)

@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.json
    place = data_manager.get(place_id, "Place")
    if place is None:
        return make_response(jsonify({"error": "Place not found"}), 404)

    if "latitude" in data and not (-90 <= data["latitude"] <= 90):
        return make_response(jsonify({"error": "Invalid latitude"}), 400)
    if "longitude" in data and not (-180 <= data["longitude"] <= 180):
        return make_response(jsonify({"error": "Invalid longitude"}), 400)
    if any(field in data and data[field] < 0 for field in ["number_of_rooms", "number_of_bathrooms", "max_guests"]):
        return make_response(jsonify({"error": "Room, bathroom, and guest capacities must be non-negative integers"}), 400)
    if "price_per_night" in data and data["price_per_night"] < 0:
        return make_response(jsonify({"error": "Price per night must be a positive value"}), 400)
    if "city_id" in data and data_manager.get(data["city_id"], "City") is None:
        return make_response(jsonify({"error": "City not found"}), 404)
    if "amenity_ids" in data:
        if not isinstance(data["amenity_ids"], list):
            return make_response(jsonify({"error": "amenity_ids should be a list"}), 400)
        for amenity_id in data["amenity_ids"]:
            if data_manager.get(amenity_id, "Amenity") is None:
                return make_response(jsonify({"error": f"Amenity {amenity_id} not found"}), 404)

    place.update(
        name=data.get("name"),
        description=data.get("description"),
        address=data.get("address"),
        city_id=data.get("city_id"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        host_id=data.get("host_id"),
        number_of_rooms=data.get("number_of_rooms"),
        number_of_bathrooms=data.get("number_of_bathrooms"),
        price_per_night=data.get("price_per_night"),
        max_guests=data.get("max_guests"),
        amenity_ids=data.get("amenity_ids")
    )
    data_manager.update(place)
    return jsonify(place.__dict__)

@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, "Place")
    if place is None:
        return make_response(jsonify({"error": "Place not found"}), 404)

    data_manager.delete(place_id, "Place")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
