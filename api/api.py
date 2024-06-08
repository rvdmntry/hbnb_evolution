#!/usr/bin/python3
"""
API for HBnB Evolution
"""

from flask import Flask, request, jsonify
from models.user import User
from persistence.data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()


@app.route('/api/v1/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Bad Request"}), 400

    try:
        user = User(email=data['email'], password=data['password'], first_name=data.get(
            'first_name', ''), last_name=data.get('last_name', ''))
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    users = [user for user in data_manager.__objects.values()
             if user['__class__'] == 'User']
    return jsonify(users)


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data_manager.get(user_id, 'User')
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Not Found"}), 404


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = data_manager.get(user_id, 'User')
    if not user:
        return jsonify({"error": "Not Found"}), 404

    if 'email' in data:
        return jsonify({"error": "Cannot change email"}), 400

    user.update(data)
    data_manager.update(user)
    return jsonify(user)


@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = data_manager.get(user_id, 'User')
    if not user:
        return jsonify({"error": "Not Found"}), 404

    data_manager.delete(user_id, 'User')
    return '', 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


@app.route('/api/v1/countries', methods=['GET'])
def get_countries():
    countries = [country for country in data_manager.__objects.values(
    ) if country['__class__'] == 'Country']
    return jsonify(countries)


@app.route('/api/v1/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    for country in data_manager.__objects.values():
        if country['__class__'] == 'Country' and country['id'] == country_code:
            return jsonify(country)
    return jsonify({"error": "Not Found"}), 404


@app.route('/api/v1/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    cities = [city for city in data_manager.__objects.values(
    ) if city['__class__'] == 'City' and city['country_id'] == country_code]
    return jsonify(cities)


@app.route('/api/v1/cities', methods=['POST'])
def create_city():
    data = request.get_json()
    if not data or 'name' not in data or 'country_id' not in data:
        return jsonify({"error": "Bad Request"}), 400

    try:
        city = City(name=data['name'], country_id=data['country_id'])
        data_manager.save(city)
        return jsonify(city.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@app.route('/api/v1/cities', methods=['GET'])
def get_cities():
    cities = [city for city in data_manager.__objects.values()
              if city['__class__'] == 'City']
    return jsonify(cities)


@app.route('/api/v1/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, 'City')
    if city:
        return jsonify(city)
    else:
        return jsonify({"error": "Not Found"}), 404


@app.route('/api/v1/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.get_json()
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({"error": "Not Found"}), 404

    city.update(data)
    data_manager.update(city)
    return jsonify(city)


@app.route('/api/v1/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({"error": "Not Found"}), 404

    data_manager.delete(city_id, 'City')
    return '', 204


@app.route('/api/v1/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Bad Request"}), 400

    try:
        amenity = Amenity(name=data['name'])
        data_manager.save(amenity)
        return jsonify(amenity.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    amenities = [amenity for amenity in data_manager.__objects.values(
    ) if amenity['__class__'] == 'Amenity']
    return jsonify(amenities)


@app.route('/api/v1/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if amenity:
        return jsonify(amenity)
    else:
        return jsonify({"error": "Not Found"}), 404


@app.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.get_json()
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        return jsonify({"error": "Not Found"}), 404

    amenity.update(data)
    data_manager.update(amenity)
    return jsonify(amenity)


@app.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        return jsonify({"error": "Not Found"}), 404

    data_manager.delete(amenity_id, 'Amenity')
    return '', 204


@app.route('/api/v1/places', methods=['POST'])
def create_place():
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data or 'address' not in data or 'city_id' not in data or 'latitude' not in data or 'longitude' not in data or 'host_id' not in data or 'number_of_rooms' not in data or 'number_of_bathrooms' not in data or 'price_per_night' not in data or 'max_guests' not in data:
        return jsonify({"error": "Bad Request"}), 400

    try:
        place = Place(name=data['name'], description=data['description'], address=data['address'], city_id=data['city_id'], latitude=data['latitude'], longitude=data['longitude'], host_id=data['host_id'],
                      number_of_rooms=data['number_of_rooms'], number_of_bathrooms=data['number_of_bathrooms'], price_per_night=data['price_per_night'], max_guests=data['max_guests'], amenities=data.get('amenities', []))
        data_manager.save(place)
        return jsonify(place.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@app.route('/api/v1/places', methods=['GET'])
def get_places():
    places = [place for place in data_manager.__objects.values()
              if place['__class__'] == 'Place']
    return jsonify(places)


@app.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if place:
        return jsonify(place)
    else:
        return jsonify({"error": "Not Found"}), 404


@app.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.get_json()
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({"error": "Not Found"}), 404

    place.update(data)
    data_manager.update(place)
    return jsonify(place)


@app.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({"error": "Not Found"}), 404

    data_manager.delete(place_id, 'Place')
    return '', 204


@app.route('/api/v1/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    data = request.get_json()
    if not data or 'user_id' not in data or 'rating' not in data or 'comment' not in data:
        return jsonify({"error": "Bad Request"}), 400

    if not data_manager.get(place_id, 'Place'):
        return jsonify({"error": "Place Not Found"}), 404

    try:
        review = Review(user_id=data['user_id'], place_id=place_id,
                        rating=data['rating'], comment=data['comment'])
        data_manager.save(review)
        return jsonify(review.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@app.route('/api/v1/users/<user_id>/reviews', methods=['GET'])
def get_reviews_by_user(user_id):
    reviews = [review for review in data_manager.__objects.values(
    ) if review['__class__'] == 'Review' and review['user_id'] == user_id]
    return jsonify(reviews)


@app.route('/api/v1/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    reviews = [review for review in data_manager.__objects.values(
    ) if review['__class__'] == 'Review' and review['place_id'] == place_id]
    return jsonify(reviews)


@app.route('/api/v1/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = data_manager.get(review_id, 'Review')
    if review:
        return jsonify(review)
    else:
        return jsonify({"error": "Not Found"}), 404


@app.route('/api/v1/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    review = data_manager.get(review_id, 'Review')
    if not review:
        return jsonify({"error": "Not Found"}), 404

    review.update(data)
    data_manager.update(review)
    return jsonify(review)


@app.route('/api/v1/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = data_manager.get(review_id, 'Review')
    if not review:
        return jsonify({"error": "Not Found"}), 404

    data_manager.delete(review_id, 'Review')
    return '', 204
