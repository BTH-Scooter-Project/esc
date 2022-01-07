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

    def tearDown(self):
        """Tear down test."""
        self.api = None


if __name__ == '__main__':
    unittest.main(verbosity=3)
