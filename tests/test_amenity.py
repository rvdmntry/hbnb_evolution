#!/usr/bin/python3
import unittest
import json
from app import app
import os
import tempfile

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.amenity_data = {
            'name': 'Test Amenity'
        }
        # Crear un archivo temporal para la base de datos
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        app.config['DATABASE'] = self.test_db.name

    def tearDown(self):
        # Clean up test data
        if os.path.exists(app.config['DATABASE']):
            os.remove(app.config['DATABASE'])

    def test_create_amenity(self):
        response = self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = response.get_json()
        self.assertIn('id', response_data)
        self.assertIsNotNone(response_data['id'])

    def test_get_amenities(self):
        self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        response = self.client.get('/amenities')
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertGreaterEqual(len(response_data), 1)

    def test_get_amenity(self):
        post_response = self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        amenity_id = post_response.get_json().get('id')
        get_response = self.client.get(f'/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 200)
        response_data = get_response.get_json()
        self.assertEqual(response_data['name'], self.amenity_data['name'])

    def test_update_amenity(self):
        post_response = self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        amenity_id = post_response.get_json().get('id')
        updated_data = {
            'name': 'Updated Amenity'
        }
        put_response = self.client.put(
            f'/amenities/{amenity_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        response_data = put_response.get_json()
        self.assertEqual(response_data['name'], 'Updated Amenity')

    def test_delete_amenity(self):
        post_response = self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        amenity_id = post_response.get_json().get('id')
        delete_response = self.client.delete(f'/amenities/{amenity_id}')
        self.assertEqual(delete_response.status_code, 204)
        get_response = self.client.get(f'/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
