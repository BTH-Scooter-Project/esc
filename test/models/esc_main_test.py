#!/usr/bin/python3
"""Test of esc main file with Handler class."""

import unittest
import sys
import os
from esc.main import esc_main

sys.path.append(os.path.dirname(__file__))


class ESCMainTestFunc(unittest.TestCase):
    """Main test function."""

    def test_esc_main(self):
        """Test esc main fuction."""
        res = esc_main()
        self.assertEqual(True, res)

if __name__ == '__main__':
    unittest.main(verbosity=3)
