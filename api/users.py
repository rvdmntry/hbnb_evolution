#!/usr/bin/python3


from flask import Flask, request, jsonify, make_response
from models.user import User
from persistence.data_manager import DataManager
import uuid
import re

app = Flask(__name__)
data_manager = DataManager()

def validate_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

def validate_user_data(data):
    if 'email' not in data or not validate_email(data['email']):
        return "Invalid or missing email", False
    if 'first_name' not in data or not isinstance(data['first_name'], str) or not data['first_name'].strip():
        return "Invalid or missing first name", False
    if 'last_name' not in data or not isinstance(data['last_name'], str) or not data['last_name'].strip():
        return "Invalid or missing last name", False
    return None, True

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    error, valid = validate_user_data(data)
    if not valid:
        return make_response(jsonify({"error": error}), 400)

    try:
        user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        data_manager.save(user)
        return make_response(jsonify(user.__dict__), 201)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 409)

@app.route('/users', methods=['GET'])
def get_users():
    users = list(data_manager.storage["User"].values())
    return jsonify([user.__dict__ for user in users])

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data_manager.get(user_id, "User")
    if user is None:
        return make_response(jsonify({"error": "User not found"}), 404)
    return jsonify(user.__dict__)

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    error, valid = validate_user_data(data)
    if not valid:
        return make_response(jsonify({"error": error}), 400)

    user = data_manager.get(user_id, "User")
    if user is None:
        return make_response(jsonify({"error": "User not found"}), 404)

    try:
        user.update(email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        data_manager.update(user)
        return jsonify(user.__dict__)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 409)

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = data_manager.get(user_id, "User")
    if user is None:
        return make_response(jsonify({"error": "User not found"}), 404)
    
    data_manager.delete(user_id, "User")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
