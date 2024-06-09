#!/usr/bin/python3
from flask import Blueprint, request, jsonify
from models.user import User
from persistence.file_storage import FileStorage
import re

user_bp = Blueprint('user_bp', __name__)
storage = FileStorage()


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'email' not in data or 'first_name' not in data or 'last_name' not in data:
        return jsonify({'error': 'Missing email, first_name, or last_name'}), 400
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    if any(user.email == data['email'] for user in storage.data.values() if isinstance(user, User)):
        return jsonify({'error': 'Email already exists'}), 409
    user = User(
        email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
    storage.save(user)
    return jsonify(user.to_dict()), 201


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = [user.to_dict()
             for user in storage.data.values() if isinstance(user, User)]
    return jsonify(users), 200


@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(user_id, 'User')
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(user_id, 'User')
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    if 'email' in data and not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    for key, value in data.items():
        setattr(user, key, value)
    user.save()
    storage.update(user)
    return jsonify(user.to_dict()), 200


@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(user_id, 'User')
    if not user:
        return jsonify({'error': 'User not found'}), 404
    storage.delete(user_id, 'User')
    return '', 204
