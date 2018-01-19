import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.test.client import JSON_CONTENT_TYPE_RE
from django.urls import reverse


class RegisterTestCase(TestCase):
    client = Client()

    def test_fail_if_invalid_json(self):
        response = self.client.post('/api-register/', data='{Some incorrect json: [}', content_type='application/json')

        self.assertEqual(response.status_code, 400, 'Incorrect json should raise 400 error')

    def test_fail_if_invalid_email(self):
        request_data = {'username': 'someusername', 'email': 'wrong_email', 'password': 'some_password'}
        response = self.client.post('/api-register/', data=json.dumps(request_data), content_type='application/json')

        self.assertEqual(response.status_code, 400, 'Incorrect email should raise 400 error')

    def test_success_if_corrent_data(self):
        request_data = {'username': 'someusername', 'email': 'test@test.pl', 'password': 'somepassword123',
                        'confirm_password': 'somepassword123'}
        response = self.client.post('/api-register/', data=json.dumps(request_data), content_type='application/json')

        self.assertEqual(response.status_code, 201, 'Correct data should successfully register new user')
        self.assertEqual(User.objects.first().username, 'someusername')
