#!/usr/bin/python3


import datetime

class User:
    def __init__(self, id, email, first_name, last_name):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Country:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name
        }

class City:
    def __init__(self, id, name, country_code):
        self.id = id
        self.name = name
        self.country_code = country_code
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country_code': self.country_code,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
