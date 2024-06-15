#!/usr/bin/python3

from flask import Flask, request, jsonify, make_response
from models.country import Country
from models.city import City
from persistence.data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()

# Pre-load countries (ISO 3166-1 alpha-2)
preloaded_countries = [
    {"code": "US", "name": "United States"},
    {"code": "CA", "name": "Canada"},
    # Add more countries as needed
]

# Ensure preloaded countries are saved correctly
for country_data in preloaded_countries:
    if data_manager.get(country_data["code"], "Country") is None:
        country = Country(code=country_data["code"], name=country_data["name"])
        data_manager.save(country)

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = data_manager.get_all("Country")
    return jsonify([country.to_dict() for country in countries])

@app.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = data_manager.get(country_code, "Country")
    if country is None:
        return make_response(jsonify({"error": "Country not found"}), 404)
    return jsonify(country.to_dict())

@app.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    country = data_manager.get(country_code, "Country")
    if country is None:
        return make_response(jsonify({"error": "Country not found"}), 404)
    cities = [city.to_dict() for city in data_manager.get_all("City") if city.country_code == country_code]
    return jsonify(cities)

@app.route('/cities', methods=['POST'])
def create_city():
    data = request.json
    if "name" not in data or not data["name"].strip():
        return make_response(jsonify({"error": "Invalid or missing city name"}), 400)
    if "country_code" not in data or data_manager.get(data["country_code"], "Country") is None:
        return make_response(jsonify({"error": "Invalid or missing country code"}), 400)

    try:
        city = City(name=data["name"], country_code=data["country_code"])
        data_manager.save(city)
        return make_response(jsonify(city.to_dict()), 201)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 409)

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = data_manager.get_all("City")
    return jsonify([city.to_dict() for city in cities])

@app.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, "City")
    if city is None:
        return make_response(jsonify({"error": "City not found"}), 404)
    return jsonify(city.to_dict())

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.json
    city = data_manager.get(city_id, "City")
    if city is None:
        return make_response(jsonify({"error": "City not found"}), 404)

    if "name" in data and not data["name"].strip():
        return make_response(jsonify({"error": "Invalid city name"}), 400)
    if "country_code" in data and data_manager.get(data["country_code"], "Country") is None:
        return make_response(jsonify({"error": "Invalid country code"}), 400)

    try:
        city.update(name=data.get("name"), country_code=data.get("country_code"))
        data_manager.update(city)
        return jsonify(city.to_dict())
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 409)

@app.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, "City")
    if city is None:
        return make_response(jsonify({"error": "City not found"}), 404)

    data_manager.delete(city_id, "City")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
