#!/usr/bin/python3
"""Main file with Handler class."""

import json
import unittest
from esc.api import Api


CONFIG_FILE = 'test/config/config.json'


def get_config(file):
    """Load config settings."""
    with open(file, 'r') as file_handle:
        return json.load(file_handle)


class TestFunc(unittest.TestCase):
    """Main test function."""

    def setUp(self):
        """Set up each test."""
        self.api = Api(1, relative_path="test/")
        self.config = get_config(CONFIG_FILE)

    def test_login(self):
        """Test api login."""
        self.api.login()
        self.assertEqual(self.config['x-access-token'], self.api.token)

    def test_rent_bike(self):
        """Test rentig a bike."""
        response = self.api.rent_bike(self.config['bikeid'])
        self.assertEqual(response.status_code, 201)
        content = response.json()['data']
        self.assertEqual(content['bikeid'], self.config['bikeid'])

    def test_rent_bike_without_token(self):
        """Test rentig a bike without token."""
        response = self.api.rent_bike_without_token(self.config['bikeid'])
        self.assertEqual(response.status_code, 201)
        content = response.json()['data']
        self.assertEqual(content['bikeid'], self.config['bikeid'])

    def test_get_rented_bikes(self):
        """Test fetching rented bike list."""
        rented_bikes = self.api.get_rented_bikes()
        self.api.get_states_for_all_bikes()
        self.assertEqual(rented_bikes[0], self.config['bikeid'])

    def tearDown(self):
        """Tear down test."""
        self.api = None


if __name__ == '__main__':
    unittest.main(verbosity=3)
