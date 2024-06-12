#!/usr/bin/python3
import unittest
import json
from app import app


class TestCountryEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_get_countries(self):
        response = self.client.get('/countries')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)

    def test_get_country(self):
        response = self.client.get('/countries/US')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'United States')

    def test_get_country_cities(self):
        response = self.client.get('/countries/US/cities')
        self.assertEqual(response.status_code, 200)


class TestCityEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.city_data = {
            'name': 'Test City',
            'country_code': 'US'
        }

    def tearDown(self):
        # Clean up test data
        import shutil
        shutil.rmtree('data/cities', ignore_errors=True)

    def test_create_city(self):
        response = self.client.post(
            '/cities', data=json.dumps(self.city_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_cities(self):
        self.client.post('/cities', data=json.dumps(self.city_data),
                         content_type='application/json')
        response = self.client.get('/cities')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_city(self):
        post_response = self.client.post(
            '/cities', data=json.dumps(self.city_data), content_type='application/json')
        city_id = post_response.json['id']
        get_response = self.client.get(f'/cities/{city_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['name'], self.city_data['name'])

    def test_update_city(self):
        post_response = self.client.post(
            '/cities', data=json.dumps(self.city_data), content_type='application/json')
        city_id = post_response.json['id']
        updated_data = {
            'name': 'Updated City',
            'country_code': 'US'
        }
        put_response = self.client.put(
            f'/cities/{city_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json['name'], 'Updated City')

    def test_delete_city(self):
        post_response = self.client.post(
            '/cities', data=json.dumps(self.city_data), content_type='application/json')
        city_id = post_response.json['id']
        delete_response = self.client.delete(f'/cities/{city_id}')
        self.assertEqual(delete_response.status_code, 204)
        get_response = self.client.get(f'/cities/{city_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
