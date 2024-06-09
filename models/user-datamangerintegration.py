#!/usr/bin/python3
"""implementation in user.py in order to use datamanager"""


from model.base_model import BaseModel

from persistence.data_manager import DataManager


class User(BaseModel):
    data_manager = DataManager()

    def __init__(self, email, password, first_name='', last_name='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if any(user['email'] == email for user in User.data_manager.__objects.values() if user['type'] == 'User'):
            raise ValueError("Email already exists")
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        User.data_manager.save(self)

    def to_dict(self):
        dict_repr = super().to_dict()
        dict_repr.update({
            'type': 'User',
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name
        })
        return dict_repr


class User(BaseModel):
    data_manager = DataManager()

    def __init__(self, email, password, first_name='', last_name='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if any(user['email'] == email for user in User.data_manager.__objects.values() if user['type'] == 'User'):
            raise ValueError("Email already exists")
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        User.data_manager.save(self)

    def to_dict(self):
        dict_repr = super().to_dict()
        dict_repr.update({
            'type': 'User',
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name
        })
        return dict_repr


class User(BaseModel):
    data_manager = DataManager()

    def __init__(self, email, password, first_name='', last_name='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if any(user['email'] == email for user in User.data_manager.__objects.values() if user['type'] == 'User'):
            raise ValueError("Email already exists")
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        User.data_manager.save(self)

    def to_dict(self):
        dict_repr = super().to_dict()
        dict_repr.update({
            'type': 'User',
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name
        })
        return dict_repr
