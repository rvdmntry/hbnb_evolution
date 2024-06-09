# models/country.py

class Country:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name
        }
