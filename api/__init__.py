from flask import Flask
from api.users import users_blueprint
from api.countries import countries_blueprint
from api.cities import cities_blueprint
from api.amenities import amenities_blueprint
from api.places import places_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(countries_blueprint)
    app.register_blueprint(cities_blueprint)
    app.register_blueprint(amenities_blueprint)
    app.register_blueprint(places_blueprint)
    return app
