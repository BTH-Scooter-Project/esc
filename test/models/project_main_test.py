#!/usr/bin/python3
"""Main file with Handler class."""

import json
import flask_unittest
from cust_iface.project import app


CONFIG_FILE = 'test/config/config.json'


def get_config(file):
    """Load config settings."""
    with open(file, 'r') as file_handle:
        return json.load(file_handle)


class ProjectMainTestCase(flask_unittest.ClientTestCase):
    """Main test function."""

    app = app
    # app.run(debug=True)

    def setUp(self, client):
        """Set up each test."""
        self.config = get_config(CONFIG_FILE)

    def test_app_1_home(self, client):
        """Test customer interface home."""
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Elsparkcykel', response.data.decode("utf-8"))

    def test_app_2_login_get(self, client):
        """Test customer interface login."""
        response = client.get('/login')
        self.assertIn(b'Login', response.data)
        self.assertIn('Sign in with Google', response.data.decode("utf-8"))

    def test_app_3_login_post(self, client):
        """Test customer interface login."""
        data = {
            "email": self.config['email'],
            "password": self.config['password']
        }
        response = client.post('/login', data=data)
        self.assertEqual(response.status_code, 302, "Redirect to /profile")

        data = {
            "email": self.config['email'],
            "password": 'wrong'
        }
        response = client.post('/login', data=data)
        self.assertEqual(response.status_code, 302, "Redirect to /profile")

    def test_app_4_profile_get_and_post(self, client):
        """Test customer interface login."""
        data = {
            "email": self.config['email'],
            "password": self.config['password']
        }
        response = client.post('/login', data=data)

        response = client.get('/profile')
        self.assertEqual(response.status_code, 200)

        data = {
            "email": self.config['email'],
            "password": self.config['password']
        }
        response = client.post('/profile')
        self.assertEqual(response.status_code, 302)

    def test_app_6_travel_get(self, client):
        """Test customer interface login."""
        data = {
            "email": self.config['email'],
            "password": self.config['password']
        }
        response = client.post('/login', data=data)
        response = client.get('/travels')
        self.assertEqual(response.status_code, 200)

        # self.assertIn(b'Login', response.data)
        # self.assertIn('Sign in with Google', response.data.decode("utf-8"))

    def test_app_7_signup_get_and_post(self, client):
        """Test customer interface login."""
        data = {
            "email": self.config['email'],
            "password": self.config['password'],
            "balance": self.config['balance'],
            "payment": self.config['payment'],
            "firstname": self.config['firstname'],
            "lastname": self.config['lastname']
        }
        response = client.get('/signup')
        self.assertEqual(response.status_code, 200)

        response = client.post('/signup', data=data)
        self.assertEqual(response.status_code, 302, "Redirect to /login")

    def test_app_8_logout(self, client):
        """Test customer interface login."""
        data = {
            "email": self.config['email'],
            "password": self.config['password']
        }
        response = client.post('/login', data=data)

        response = client.get('/logout')
        self.assertEqual(response.status_code, 302, "Redirect to /")

    def test_app_9_callback(self, client):
        """Test customer interface login."""
        response = client.get('/login/callback')
        self.assertEqual(response.status_code, 302, "Redirect to /profile")
