# api/cities.py

from flask import Blueprint, request, jsonify
from models.data_manager import DataManager
from models.city import City
from models.country import Country
from models.country import countries
from models.validation import validate_city_payload
from flask import jsonify
from flask import Blueprint  # Import the Blueprint class from the flask module

cities_blueprint = Blueprint('cities', __name__)
data_manager = DataManager()

# Validation function
...

# POST /cities: Create a new city


@cities_blueprint.route('/cities', methods=['POST'])
def create_city():
    data = request.get_json()
    is_valid, message = validate_city_payload(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    existing_cities = data_manager.get_all(City)
    if any(city.name == data["name"] and city.country_code == data["country_code"].upper() for city in existing_cities):
        return jsonify({"error": "City name already exists in the specified country"}), 409

    city = City(name=data["name"], country_code=data["country_code"].upper())
    data_manager.save(city)


return jsonify(city.to_dict()), 201
return jsonify(city.to_dict()), 201

# GET /cities: Retrieve all cities


@cities_blueprint.route('/cities', methods=['GET'])
def get_cities():
    cities = [city.to_dict() for city in data_manager.get_all(City)]
    return jsonify(cities), 200

# GET /cities/<city_id>: Retrieve details of a specific city


@cities_blueprint.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, City)
    if city:
        return jsonify(city.to_dict()), 200
    return jsonify({"error": "City not found"}), 404

# PUT /cities/<city_id>: Update an existing city’s information


@cities_blueprint.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = data_manager.get(city_id, City)
    if not city:
        return jsonify({"error": "City not found"}), 404

    data = request.get_json()
    is_valid, message = validate_city_payload(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    if "name" in data:
        existing_cities = data_manager.get_all(City)
        if any(existing_city.name == data["name"] and existing_city.country_code == city.country_code and existing_city.id != city.id for existing_city in existing_cities):
            return jsonify({"error": "City name already exists in the specified country"}), 409

    city.update(**data)
    data_manager.update(city)
    return jsonify(city.to_dict()), 200

# DELETE /cities/<city_id>: Delete a specific city


@cities_blueprint.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, City)
    if not city:
        return jsonify({"error": "City not found"}), 404

    data_manager.delete(city_id, City)
    return '', 204
