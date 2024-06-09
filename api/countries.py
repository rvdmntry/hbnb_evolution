# api/countries.py

from flask import Blueprint, jsonify

countries_blueprint = Blueprint('countries', __name__)

# Pre-load country data based on ISO 3166-1 alpha-2 codification
COUNTRIES = {
    "US": "United States",
    "CA": "Canada",
    "GB": "United Kingdom",
    # Add more countries as needed
}


@countries_blueprint.route('/countries', methods=['GET'])
def get_countries():
    return jsonify([{'code': code, 'name': name} for code, name in COUNTRIES.items()]), 200


@countries_blueprint.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country_name = COUNTRIES.get(country_code.upper())
    if not country_name:
        return jsonify({"error": "Country not found"}), 404
    return jsonify({'code': country_code.upper(), 'name': country_name}), 200


@countries_blueprint.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    # Retrieve all cities from the data manager and filter by country code
    cities = [city.to_dict() for city in data_manager.get_all(
        City) if city.country_code == country_code.upper()]
    return jsonify(cities), 200
