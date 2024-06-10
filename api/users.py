from flask_restx import Namespace, Resource, fields
from flask import request
from persistence.data_manager import DataManager
from models.user import User

api = Namespace('users', description='User operations')

data_manager = DataManager()

user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The user unique identifier'),
    'email': fields.String(required=True, description='The user email'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'created_at': fields.String(readOnly=True, description='The user creation date'),
    'updated_at': fields.String(readOnly=True, description='The user update date')
})


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = data_manager.get_all('User')
        return users

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.json
        if 'email' not in data or not data['email']:
            api.abort(400, 'Email is required')
        if 'first_name' not in data or not data['first_name']:
            api.abort(400, 'First name is required')
        if 'last_name' not in data or not data['last_name']:
            api.abort(400, 'Last name is required')

        if data_manager.find_by_email(data['email']):
            api.abort(409, 'Email already exists')

        user = User(email=data['email'], password='',
                    first_name=data['first_name'], last_name=data['last_name'])
        data_manager.save(user)
        return user, 201


@api.route('/<string:id>')
@api.response(404, 'User not found')
@api.param('id', 'The user identifier')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, id):
        """Fetch a user given its identifier"""
        user = data_manager.get(id, 'User')
        if not user:
            api.abort(404, 'User not found')
        return user

    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, id):
        """Update a user given its identifier"""
        data = request.json
        user = data_manager.get(id, 'User')
        if not user:
            api.abort(404, 'User not found')

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        data_manager.update(user)
        return user

    @api.doc('delete_user')
    @api.response(204, 'User deleted')
    def delete(self, id):
        """Delete a user given its identifier"""
        user = data_manager.get(id, 'User')
        if not user:
            api.abort(404, 'User not found')
        data_manager.delete(id, 'User')
        return '', 204
