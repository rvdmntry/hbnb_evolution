#!/usr/bin/python3

from datetime import datetime
import uuid

class User:
    emails = set()

    def __init__(self, email, first_name, last_name):
        if email in User.emails:
            raise ValueError("Email already exists")
        self.id = str(uuid.uuid4())  # Ensure the ID is a string
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        User.emails.add(email)

    def update(self, first_name=None, last_name=None, email=None):
        if email and email != self.email:
            if email in User.emails:
                raise ValueError("Email already exists")
            User.emails.remove(self.email)
            self.email = email
            User.emails.add(email)
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),  # Serialize datetime to string
            'updated_at': self.updated_at.isoformat()   # Serialize datetime to string
        }

    @classmethod
    def clear_emails(cls):
        cls.emails.clear()
