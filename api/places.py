from flask_restx import Namespace, Resource, fields
from flask import request
from persistence.data_manager import DataManager
from models.place import Place

api = Namespace('places', description='Place operations')

data_manager = DataManager()

place_model = api.model('Place', {
    'id': fields.String(readOnly=True, description='The place unique identifier'),
    'name': fields.String(required=True, description='The place name'),
    'description': fields.String(required=True, description='The place description'),
    'address': fields.String(required=True, description='The place address'),
    'city_id': fields.String(required=True, description='The city identifier'),
    'latitude': fields.Float(required=True, description='The place latitude'),
    'longitude': fields.Float(required=True, description='The place longitude'),
    'host_id': fields.String(required=True, description='The host identifier'),
    'number_of_rooms': fields.Integer(required=True, description='The number of rooms'),
    'number_of_bathrooms': fields.Integer(required=True, description='The number of bathrooms'),
    'price_per_night': fields.Float(required=True, description='The price per night'),
    'max_guests': fields.Integer(required=True, description='The maximum number of guests'),
    'amenity_ids': fields.List(fields.String, required=True, description='The list of amenity identifiers'),
    'created_at': fields.String(readOnly=True, description='The place creation date'),
    'updated_at': fields.String(readOnly=True, description='The place update date')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        places = data_manager.get_all('Place')
        return places

    @api.doc('create_place')
    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = request.json
        required_fields = ['name', 'description', 'address', 'city_id', 'latitude', 'longitude', 'host_id',
                           'number_of_rooms', 'number_of_bathrooms', 'price_per_night', 'max_guests', 'amenity_ids']

        for field in required_fields:
            if field not in data:
                api.abort(400, f'{field} is required')

        # Validate city_id
        if not data_manager.find_by_id(data['city_id'], 'City'):
            api.abort(400, 'Invalid city_id')

        # Validate host_id
        if not data_manager.find_by_id(data['host_id'], 'User'):
            api.abort(400, 'Invalid host_id')

        # Validate amenity_ids
        for amenity_id in data['amenity_ids']:
            if not data_manager.find_by_id(amenity_id, 'Amenity'):
                api.abort(400, f'Invalid amenity_id: {amenity_id}')

        place = Place(**data)
        data_manager.save(place)
        return place, 201


@api.route('/<string:id>')
@api.response(404, 'Place not found')
@api.param('id', 'The place identifier')
class Place(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_model)
    def get(self, id):
        """Fetch a place given its identifier"""
        place = data_manager.get(id, 'Place')
        if not place:
            api.abort(404, 'Place not found')
        return place

    @api.doc('update_place')
    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, id):
        """Update a place given its identifier"""
        data = request.json
        place = data_manager.get(id, 'Place')
        if not place:
            api.abort(404, 'Place not found')

        if 'city_id' in data and not data_manager.find_by_id(data['city_id'], 'City'):
            api.abort(400, 'Invalid city_id')

        if 'host_id' in data and not data_manager.find_by_id(data['host_id'], 'User'):
            api.abort(400, 'Invalid host_id')

        if 'amenity_ids' in data:
            for amenity_id in data['amenity_ids']:
                if not data_manager.find_by_id(amenity_id, 'Amenity'):
                    api.abort(400, f'Invalid amenity_id: {amenity_id}')

        for key, value in data.items():
            setattr(place, key, value)

        data_manager.update(place)
        return place

    @api.doc('delete_place')
    @api.response(204, 'Place deleted')
    def delete(self, id):
        """Delete a place given its identifier"""
        place = data_manager.get(id, 'Place')
        if not place:
            api.abort(404, 'Place not found')
        data_manager.delete(id, 'Place')
        return '', 204
