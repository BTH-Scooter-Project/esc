#!/usr/bin/python3
"""Main esc test file with Handler class."""

import json
import unittest
import sys
import os
from esc.esc import ESCEmulator

sys.path.append(os.path.dirname(__file__))

CONFIG_FILE = 'test/config/config.json'


def get_config(file):
    """Load config settings."""
    with open(file, 'r') as file_handle:
        return json.load(file_handle)


class ESCTestFunc(unittest.TestCase):
    """Main test function."""

    def setUp(self):
        """Set up each test."""
        self.esc_emulator = ESCEmulator(1, test=True)
        
    def test_1_calc_path_distances(self):
        """Test fuction calc_path_distances."""
        res = self.esc_emulator.ride_bike()
        self.assertEqual(False, res['finished'])
        # self.assertGreaterEqual(0, self.esc_emulator.calc_path_distances())

    def tearDown(self):
        """Tear down test."""
        self.esc_emulator = None


if __name__ == '__main__':
    unittest.main(verbosity=3)
