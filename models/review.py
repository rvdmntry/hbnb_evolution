#!/usr/bin/python3
import os
import json
from .base_model import BaseModel
from .data_manager import DataManager

data_manager = DataManager()


class Review(BaseModel):
    def __init__(self, place_id, user_id, rating, comment):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment
        })
        return review_dict

    def save(self):
        data_manager.save(self)

    @staticmethod
    def get(review_id):
        review_dict = data_manager.get(review_id, 'review')
        if review_dict:
            review = Review(
                place_id=review_dict['place_id'],
                user_id=review_dict['user_id'],
                rating=review_dict['rating'],
                comment=review_dict['comment']
            )
            review.id = review_dict['id']
            review.created_at = review_dict['created_at']
            review.updated_at = review_dict['updated_at']
            return review
        return None

    @staticmethod
    def get_all():
        reviews = []
        review_files = os.listdir('data/reviews')
        for review_file in review_files:
            with open(os.path.join('data/reviews', review_file), 'r') as file:
                review_dict = json.load(file)
                review = Review(
                    place_id=review_dict['place_id'],
                    user_id=review_dict['user_id'],
                    rating=review_dict['rating'],
                    comment=review_dict['comment']
                )
                review.id = review_dict['id']
                review.created_at = review_dict['created_at']
                review.updated_at = review_dict['updated_at']
                reviews.append(review)
        return reviews

    @staticmethod
    def delete(review_id):
        data_manager.delete(review_id, 'review')

    @staticmethod
    def get_by_user(user_id):
        return [review for review in Review.get_all() if review.user_id == user_id]

    @staticmethod
    def get_by_place(place_id):
        return [review for review in Review.get_all() if review.place_id == place_id]
