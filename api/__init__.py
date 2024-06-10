from flask import Flask
from flask_restx import Api

from api.users import api as users_ns
from api.amenities import api as amenities_ns
from api.places import api as places_ns

app = Flask(__name__)
api = Api(app, version='1.0', title='HBnB API',
          description='A simple HBnB API')

api.add_namespace(users_ns, path='/users')
api.add_namespace(amenities_ns, path='/amenities')
api.add_namespace(places_ns, path='/places')

if __name__ == '__main__':
    app.run(debug=True)
