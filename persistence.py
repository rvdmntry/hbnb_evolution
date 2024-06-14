#!/usr/bin/python3


from models.user import User

class DataManager:
    def __init__(self):
        self.storage = {
            'User': {}
        }

    def save(self, entity):
        entity_type = type(entity).__name__
        self.storage[entity_type][entity.id] = entity

    def get(self, entity_id, entity_type):
        return self.storage[entity_type].get(entity_id)

    def get_all(self, entity_type):
        return list(self.storage[entity_type].values())

    def update(self, entity):
        entity_type = type(entity).__name__
        self.storage[entity_type][entity.id] = entity

    def delete(self, entity_id, entity_type):
        if entity_id in self.storage[entity_type]:
            del self.storage[entity_type][entity_id]

    def is_email_unique(self, email):
        for user in self.storage['User'].values():
            if user.email == email:
                return False
        return True
