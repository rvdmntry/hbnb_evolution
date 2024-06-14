#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from flask_restx import Api, Resource, fields
from models.data_manager import DataManager
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
api = Api(app, version='1.0', title='HBnB API',
          description='A simple API for HBnB application')
api = Api(app, version='1.0', title='HBnB API',
          description='A simple API for HBnB application')

data_manager = DataManager()

# Namespaces
country_ns = api.namespace('countries', description='Country operations')
city_ns = api.namespace('cities', description='City operations')
amenity_ns = api.namespace('amenities', description='Amenity operations')
place_ns = api.namespace('places', description='Place operations')
user_ns = api.namespace('users', description='User operations')
review_ns = api.namespace('reviews', description='Review operations')

# Models
country_model = api.model('Country', {
    'code': fields.String(readOnly=True, description='The unique code of the country'),
    'name': fields.String(required=True, description='Country name')
})

city_model = api.model('City', {
    'id': fields.String(readOnly=True, description='The unique identifier of a city'),
    'name': fields.String(required=True, description='City name'),
    'country_code': fields.String(required=True, description='Country code'),
    'created_at': fields.String(readOnly=True, description='City creation timestamp'),
    'updated_at': fields.String(readOnly=True, description='City update timestamp')
})

amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True, description='The unique identifier of an amenity'),
    'name': fields.String(required=True, description='Amenity name'),
    'created_at': fields.String(readOnly=True, description='Amenity creation timestamp'),
    'updated_at': fields.String(readOnly=True, description='Amenity update timestamp')
})

place_model = api.model('Place', {
    'id': fields.String(readOnly=True, description='The unique identifier of a place'),
    'name': fields.String(required=True, description='Place name'),
    'description': fields.String(required=True, description='Place description'),
    'address': fields.String(required=True, description='Place address'),
    'city_id': fields.String(required=True, description='City ID'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'host_id': fields.String(required=True, description='Host ID'),
    'number_of_rooms': fields.Integer(required=True, description='Number of rooms'),
    'number_of_bathrooms': fields.Integer(required=True, description='Number of bathrooms'),
    'price_per_night': fields.Float(required=True, description='Price per night'),
    'max_guests': fields.Integer(required=True, description='Maximum number of guests'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs'),
    'created_at': fields.String(readOnly=True, description='Place creation timestamp'),
    'updated_at': fields.String(readOnly=True, description='Place update timestamp')
})

user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier of a user'),
    'email': fields.String(required=True, description='User email'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'created_at': fields.String(readOnly=True, description='User creation timestamp'),
    'updated_at': fields.String(readOnly=True, description='User update timestamp')
})

review_model = api.model('Review', {
    'id': fields.String(readOnly=True, description='The unique identifier of a review'),
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id': fields.String(required=True, description='User ID'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'comment': fields.String(required=True, description='Review comment'),
    'created_at': fields.String(readOnly=True, description='Review creation timestamp'),
    'updated_at': fields.String(readOnly=True, description='Review update timestamp')
})

# Endpoints


@country_ns.route('/')
class CountryList(Resource):
    @country_ns.doc('list_countries')
    @country_ns.marshal_list_with(country_model)
    def get(self):
        return data_manager.get_all_countries()


@country_ns.route('/<string:country_code>')
@country_ns.response(404, 'Country not found')
@country_ns.param('country_code', 'The country code')
class Country(Resource):
    @country_ns.doc('get_country')
    @country_ns.marshal_with(country_model)
    def get(self, country_code):
        country = data_manager.get_country(country_code)
        if not country:
            api.abort(404)
        return country


@country_ns.route('/<string:country_code>/cities')
@country_ns.response(404, 'Country not found')
@country_ns.param('country_code', 'The country code')
class CountryCities(Resource):
    @country_ns.doc('list_country_cities')
    @country_ns.marshal_list_with(city_model)
    def get(self, country_code):
        country = data_manager.get_country(country_code)
        if not country:
            api.abort(404)
        cities = [city.to_dict() for city in City.get_all()
                  if city.country_code == country_code]
        return cities


@city_ns.route('/')
class CityList(Resource):
    @city_ns.doc('list_cities')
    @city_ns.marshal_list_with(city_model)
    def get(self):
        return [city.to_dict() for city in City.get_all()]

    @city_ns.doc('create_city')
    @city_ns.expect(city_model)
    @city_ns.marshal_with(city_model, code=201)
    def post(self):
        data = request.json
        if not data_manager.get_country(data['country_code']):
            api.abort(400, "Invalid country code")
        for city in City.get_all():
            if city.name == data['name'] and city.country_code == data['country_code']:
                api.abort(
                    409, "City name already exists in the specified country")
        city = City(name=data['name'], country_code=data['country_code'])
        city.save()
        return city, 201


@city_ns.route('/<string:city_id>')
@city_ns.response(404, 'City not found')
@city_ns.param('city_id', 'The city identifier')
class City(Resource):
    @city_ns.doc('get_city')
    @city_ns.marshal_with(city_model)
    def get(self, city_id):
        city = City.get(city_id)
        if not city:
            api.abort(404)
        return city

    @city_ns.doc('update_city')
    @city_ns.expect(city_model)
    @city_ns.marshal_with(city_model)
    def put(self, city_id):
        data = request.json
        city = City.get(city_id)
        if not city:
            api.abort(404)
        if not data_manager.get_country(data['country_code']):
            api.abort(400, "Invalid country code")
        for existing_city in City.get_all():
            if existing_city.name == data['name'] and existing_city.country_code == data['country_code'] and existing_city.id != city_id:
                api.abort(
                    409, "City name already exists in the specified country")
        city.name = data['name']
        city.country_code = data['country_code']
        city.save()
        return city

    @city_ns.doc('delete_city')
    @city_ns.response(204, 'City deleted')
    def delete(self, city_id):
        city = City.get(city_id)
        if not city:
            api.abort(404)
        City.delete(city_id)
        return '', 204


@amenity_ns.route('/')
class AmenityList(Resource):
    @amenity_ns.doc('list_amenities')
    @amenity_ns.marshal_list_with(amenity_model)
    def get(self):
        return [amenity.to_dict() for amenity in Amenity.get_all()]

    @amenity_ns.doc('create_amenity')
    @amenity_ns.expect(amenity_model)
    @amenity_ns.marshal_with(amenity_model, code=201)
    def post(self):
        data = request.json
        for amenity in Amenity.get_all():
            if amenity.name == data['name']:
                api.abort(409, "Amenity name already exists")
        amenity = Amenity(name=data['name'])
        amenity.save()
        return amenity, 201


@amenity_ns.route('/<string:amenity_id>')
@amenity_ns.response(404, 'Amenity not found')
@amenity_ns.param('amenity_id', 'The amenity identifier')
class Amenity(Resource):
    @amenity_ns.doc('get_amenity')
    @amenity_ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = Amenity.get(amenity_id)
        if not amenity:
            api.abort(404)
        return amenity

    @amenity_ns.doc('update_amenity')
    @amenity_ns.expect(amenity_model)
    @amenity_ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        data = request.json
        amenity = Amenity.get(amenity_id)
        if not amenity:
            api.abort(404)
        for existing_amenity in Amenity.get_all():
            if existing_amenity.name == data['name'] and existing_amenity.id != amenity_id:
                api.abort(409, "Amenity name already exists")
        amenity.name = data['name']
        amenity.save()
        return amenity

    @amenity_ns.doc('delete_amenity')
    @amenity_ns.response(204, 'Amenity deleted')
    def delete(self, amenity_id):
        amenity = Amenity.get(amenity_id)
        if not amenity:
            api.abort(404)
        Amenity.delete(amenity_id)
        return '', 204


@place_ns.route('/')
class PlaceList(Resource):
    @place_ns.doc('list_places')
    @place_ns.marshal_list_with(place_model)
    def get(self):
        return [place.to_dict() for place in Place.get_all()]

    @place_ns.doc('create_place')
    @place_ns.expect(place_model)
    @place_ns.marshal_with(place_model, code=201)
    def post(self):
        data = request.json
        # Validate city_id
        if not City.get(data['city_id']):
            api.abort(400, "Invalid city ID")
        # Validate amenities
        for amenity_id in data['amenity_ids']:
            if not Amenity.get(amenity_id):
                api.abort(400, "Invalid amenity ID")
        place = Place(
            name=data['name'],
            description=data['description'],
            address=data['address'],
            city_id=data['city_id'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            host_id=data['host_id'],
            number_of_rooms=data['number_of_rooms'],
            number_of_bathrooms=data['number_of_bathrooms'],
            price_per_night=data['price_per_night'],
            max_guests=data['max_guests'],
            amenity_ids=data['amenity_ids']
        )
        place.save()
        return place, 201


@place_ns.route('/<string:place_id>')
@place_ns.response(404, 'Place not found')
@place_ns.param('place_id', 'The place identifier')
class Place(Resource):
    @place_ns.doc('get_place')
    @place_ns.marshal_with(place_model)
    def get(self, place_id):
        place = Place.get(place_id)
        if not place:
            api.abort(404)
        return place

    @place_ns.doc('update_place')
    @place_ns.expect(place_model)
    @place_ns.marshal_with(place_model)
    def put(self, place_id):
        data = request.json
        place = Place.get(place_id)
        if not place:
            api.abort(404)
        # Validate city_id
        if not City.get(data['city_id']):
            api.abort(400, "Invalid city ID")
        # Validate amenities
        for amenity_id in data['amenity_ids']:
            if not Amenity.get(amenity_id):
                api.abort(400, "Invalid amenity ID")
        place.name = data['name']
        place.description = data['description']
        place.address = data['address']
        place.city_id = data['city_id']
        place.latitude = data['latitude']
        place.longitude = data['longitude']
        place.host_id = data['host_id']
        place.number_of_rooms = data['number_of_rooms']
        place.number_of_bathrooms = data['number_of_bathrooms']
        place.price_per_night = data['price_per_night']
        place.max_guests = data['max_guests']
        place.amenity_ids = data['amenity_ids']
        place.save()
        return place

    @place_ns.doc('delete_place')
    @place_ns.response(204, 'Place deleted')
    def delete(self, place_id):
        place = Place.get(place_id)
        if not place:
            api.abort(404)
        Place.delete(place_id)
        return '', 204


@user_ns.route('/')
class UserList(Resource):
    @user_ns.doc('list_users')
    @user_ns.marshal_list_with(user_model)
    def get(self):
        return [user.to_dict() for user in User.get_all()]

    @user_ns.doc('create_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        data = request.json
        if User.get_by_email(data['email']):
            api.abort(409, "Email already exists")
        user = User(
            email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.save()
        return user, 201


@user_ns.route('/<string:user_id>')
@user_ns.response(404, 'User not found')
@user_ns.param('user_id', 'The user identifier')
class User(Resource):
    @user_ns.doc('get_user')
    @user_ns.marshal_with(user_model)
    def get(self, user_id):
        user = User.get(user_id)
        if not user:
            api.abort(404)
        return user

    @user_ns.doc('update_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model)
    def put(self, user_id):
        data = request.json
        user = User.get(user_id)
        if not user:
            api.abort(404)
        if data['email'] != user.email and User.get_by_email(data['email']):
            api.abort(409, "Email already exists")
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        return user

    @user_ns.doc('delete_user')
    @user_ns.response(204, 'User deleted')
    def delete(self, user_id):
        user = User.get(user_id)
        if not user:
            api.abort(404)
        User.delete(user_id)
        return '', 204


@review_ns.route('/places/<string:place_id>')
class PlaceReviewList(Resource):
    @review_ns.doc('list_place_reviews')
    @review_ns.marshal_list_with(review_model)
    def get(self, place_id):
        if not Place.get(place_id):
            api.abort(404, "Place not found")
        return [review.to_dict() for review in Review.get_by_place(place_id)]

    @review_ns.doc('create_review')
    @review_ns.expect(review_model)
    @review_ns.marshal_with(review_model, code=201)
    def post(self, place_id):
        data = request.json
        if not Place.get(place_id):
            api.abort(404, "Place not found")
        if not User.get(data['user_id']):
            api.abort(400, "Invalid user ID")
        if not (1 <= data['rating'] <= 5):
            api.abort(400, "Rating must be between 1 and 5")
        place = Place.get(place_id)
        if place.host_id == data['user_id']:
            api.abort(400, "Host cannot review their own place")
        review = Review(
            place_id=place_id,
            user_id=data['user_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        review.save()
        return review, 201


@review_ns.route('/users/<string:user_id>')
class UserReviewList(Resource):
    @review_ns.doc('list_user_reviews')
    @review_ns.marshal_list_with(review_model)
    def get(self, user_id):
        if not User.get(user_id):
            api.abort(404, "User not found")
        return [review.to_dict() for review in Review.get_by_user(user_id)]


@review_ns.route('/<string:review_id>')
@review_ns.response(404, 'Review not found')
@review_ns.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @review_ns.doc('get_review')
    @review_ns.marshal_with(review_model)
    def get(self, review_id):
        review = Review.get(review_id)
        if not review:
            api.abort(404)
        return review

    @review_ns.doc('update_review')
    @review_ns.expect(review_model)
    @review_ns.marshal_with(review_model)
    def put(self, review_id):
        data = request.json
        review = Review.get(review_id)
        if not review:
            api.abort(404)
        if not (1 <= data['rating'] <= 5):
            api.abort(400, "Rating must be between 1 and 5")
        review.rating = data['rating']
        review.comment = data['comment']
        review.save()
        return review

    @review_ns.doc('delete_review')
    @review_ns.response(204, 'Review deleted')
    def delete(self, review_id):
        review = Review.get(review_id)
        if not review:
            api.abort(404)
        Review.delete(review_id)
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
