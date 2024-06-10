from flask_restx import Namespace, Resource, fields
from flask import request
from persistence.data_manager import DataManager
from models.amenity import Amenity

api = Namespace('amenities', description='Amenity operations')

data_manager = DataManager()

amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True, description='The amenity unique identifier'),
    'name': fields.String(required=True, description='The amenity name'),
    'created_at': fields.String(readOnly=True, description='The amenity creation date'),
    'updated_at': fields.String(readOnly=True, description='The amenity update date')
})


@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        amenities = data_manager.get_all('Amenity')
        return amenities

    @api.doc('create_amenity')
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = request.json
        if 'name' not in data or not data['name']:
            api.abort(400, 'Name is required')

        if data_manager.find_by_name(data['name'], 'Amenity'):
            api.abort(409, 'Amenity with this name already exists')

        amenity = Amenity(name=data['name'])
        data_manager.save(amenity)
        return amenity, 201


@api.route('/<string:id>')
@api.response(404, 'Amenity not found')
@api.param('id', 'The amenity identifier')
class Amenity(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    def get(self, id):
        """Fetch an amenity given its identifier"""
        amenity = data_manager.get(id, 'Amenity')
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, id):
        """Update an amenity given its identifier"""
        data = request.json
        amenity = data_manager.get(id, 'Amenity')
        if not amenity:
            api.abort(404, 'Amenity not found')

        if 'name' in data and data['name']:
            if data_manager.find_by_name(data['name'], 'Amenity'):
                api.abort(409, 'Amenity with this name already exists')
            amenity.name = data['name']

        data_manager.update(amenity)
        return amenity

    @api.doc('delete_amenity')
    @api.response(204, 'Amenity deleted')
    def delete(self, id):
        """Delete an amenity given its identifier"""
        amenity = data_manager.get(id, 'Amenity')
        if not amenity:
            api.abort(404, 'Amenity not found')
        data_manager.delete(id, 'Amenity')
        return '', 204
