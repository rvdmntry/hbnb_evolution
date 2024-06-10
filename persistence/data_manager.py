# Add these methods to the DataManager class

class DataManager(IPersistenceManager):
    # existing methods...

    def get_all(self, entity_type):
        return [entity for key, entity in self.__objects.items() if key.startswith(entity_type)]

    def find_by_email(self, email):
        for key, entity in self.__objects.items():
            if key.startswith('User') and entity.email == email:
                return entity
        return None
