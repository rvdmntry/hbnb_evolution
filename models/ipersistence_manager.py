#!/usr/bin/python3
from abc import ABC, abstractmethod


class IPersistenceManager(ABC):

    @abstractmethod
    def save(self, entity):
        """Save an entity to storage"""
        pass

    @abstractmethod
    def get(self, entity_id, entity_type):
        """Retrieve an entity by its ID and type"""
        pass

    @abstractmethod
    def update(self, entity):
        """Update an entity in storage"""
        pass

    @abstractmethod
    def delete(self, entity_id, entity_type):
        """Delete an entity from storage"""
        pass
