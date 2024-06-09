# api/users.py

from flask import Blueprint, request, jsonify
from models.data_manager import DataManager
from models.user import User
import re

users_blueprint = Blueprint('users', __name__)
data_manager = DataManager()

# Validation function


def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

# POST /users: Create a new user


@users_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password", "first_name", "last_name")):
        return jsonify({"error": "Missing required fields"}), 400

    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    existing_users = data_manager.get_all(User)
    if any(user.email == data["email"] for user in existing_users):
        return jsonify({"error": "Email already exists"}), 409

    user = User(email=data["email"], password=data["password"],
                first_name=data["first_name"], last_name=data["last_name"])
    data_manager.save(user)
    return jsonify(user.to_dict()), 201

# GET /users: Retrieve a list of all users


@users_blueprint.route('/users', methods=['GET'])
def get_users():
    users = [user.to_dict() for user in data_manager.get_all(User)]
    return jsonify(users), 200

# GET /users/<user_id>: Retrieve details of a specific user


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data_manager.get(user_id, User)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

# PUT /users/<user_id>: Update an existing user


@users_blueprint.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = data_manager.get(user_id, User)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "email" in data and not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    if "email" in data:
        existing_users = data_manager.get_all(User)
        if any(existing_user.email == data["email"] and existing_user.id != user.id for existing_user in existing_users):
            return jsonify({"error": "Email already exists"}), 409

    user.update(**data)
    data_manager.update(user)
    return jsonify(user.to_dict()), 200

# DELETE /users/<user_id>: Delete a user


@users_blueprint.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = data_manager.get(user_id, User)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data_manager.delete(user_id, User)
    return '', 204
