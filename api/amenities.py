# api/amenities.py

from flask import Blueprint, request, jsonify
from models.data_manager import DataManager
from models.amenity.py import Amenity

amenities_blueprint = Blueprint('amenities', __name__)
data_manager = DataManager()

# Validation function


def validate_amenity_payload(data):
    if "name" not in data or not data["name"]:
        return False, "Missing or empty required field: name"
    return True, ""

# POST /amenities: Create a new amenity


@amenities_blueprint.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    is_valid, message = validate_amenity_payload(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    existing_amenities = data_manager.get_all(Amenity)
    if any(amenity.name == data["name"] for amenity in existing_amenities):
        return jsonify({"error": "Amenity name already exists"}), 409

    amenity = Amenity(name=data["name"])
    data_manager.save(amenity)
    return jsonify(amenity.to_dict()), 201

# GET /amenities: Retrieve a list of all amenities


@amenities_blueprint.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = [amenity.to_dict()
                 for amenity in data_manager.get_all(Amenity)]
    return jsonify(amenities), 200

# GET /amenities/<amenity_id>: Retrieve detailed information about a specific amenity


@amenities_blueprint.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, Amenity)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    return jsonify({"error": "Amenity not found"}), 404

# PUT /amenities/<amenity_id>: Update an existing amenity’s information


@amenities_blueprint.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, Amenity)
    if not amenity:
        return jsonify({"error": "Amenity not found"}), 404

    data = request.get_json()
    is_valid, message = validate_amenity_payload(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    if "name" in data:
        existing_amenities = data_manager.get_all(Amenity)
        if any(existing_amenity.name == data["name"] and existing_amenity.id != amenity.id for existing_amenity in existing_amenities):
            return jsonify({"error": "Amenity name already exists"}), 409

    amenity.update(**data)
    data_manager.update(amenity)
    return jsonify(amenity.to_dict()), 200

# DELETE /amenities/<amenity_id>: Delete a specific amenity


@amenities_blueprint.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, Amenity)
    if not amenity:
        return jsonify({"error": "Amenity not found"}), 404

    data_manager.delete(amenity_id, Amenity)
    return '', 204
