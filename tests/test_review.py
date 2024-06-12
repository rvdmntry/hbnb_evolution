#!/usr/bin/python3
import unittest
import json
from app import app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user_response = self.client.post(
            '/users', data=json.dumps(self.user_data), content_type='application/json')
        self.user_id = self.user_response.json['id']
        self.city_data = {
            'name': 'Test City',
            'country_code': 'US'
        }
        self.city_response = self.client.post(
            '/cities', data=json.dumps(self.city_data), content_type='application/json')
        self.city_id = self.city_response.json['id']
        self.place_data = {
            'name': 'Test Place',
            'description': 'A place for testing',
            'address': '123 Test St',
            'city_id': self.city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': self.user_id,
            'number_of_rooms': 2,
            'number_of_bathrooms': 1,
            'price_per_night': 100.0,
            'max_guests': 4,
            'amenity_ids': []
        }
        self.place_response = self.client.post(
            '/places', data=json.dumps(self.place_data), content_type='application/json')
        self.place_id = self.place_response.json['id']
        self.review_data = {
            'user_id': self.user_id,
            'rating': 5,
            'comment': 'Great place!'
        }

    def tearDown(self):
        # Clean up test data
        import shutil
        shutil.rmtree('data/reviews', ignore_errors=True)
        shutil.rmtree('data/places', ignore_errors=True)
        shutil.rmtree('data/cities', ignore_errors=True)
        shutil.rmtree('data/users', ignore_errors=True)

    def test_create_review(self):
        response = self.client.post(f'/places/{self.place_id}/reviews', data=json.dumps(
            self.review_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_reviews_by_user(self):
        self.client.post(f'/places/{self.place_id}/reviews', data=json.dumps(
            self.review_data), content_type='application/json')
        response = self.client.get(f'/users/{self.user_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_reviews_by_place(self):
        self.client.post(f'/places/{self.place_id}/reviews', data=json.dumps(
            self.review_data), content_type='application/json')
        response = self.client.get(f'/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_review(self):
        post_response = self.client.post(
            f'/places/{self.place_id}/reviews', data=json.dumps(self.review_data), content_type='application/json')
        review_id = post_response.json['id']
        get_response = self.client.get(f'/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.json['comment'], self.review_data['comment'])

    def test_update_review(self):
        post_response = self.client.post(
            f'/places/{self.place_id}/reviews', data=json.dumps(self.review_data), content_type='application/json')
        review_id = post_response.json['id']
        updated_data = {
            'user_id': self.user_id,
            'rating': 4,
            'comment': 'Good place!'
        }
        put_response = self.client.put(
            f'/reviews/{review_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json['comment'], 'Good place!')

    def test_delete_review(self):
        post_response = self.client.post(
            f'/places/{self.place_id}/reviews', data=json.dumps(self.review_data), content_type='application/json')
        review_id = post_response.json['id']
        delete_response = self.client.delete(f'/reviews/{review_id}')
        self.assertEqual(delete_response.status_code, 204)
        get_response = self.client.get(f'/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
