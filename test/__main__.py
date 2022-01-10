"""__main__.py file."""

import sys
import unittest
import coverage

sys.path.append('../esc')
sys.path.append('../cust_iface')


def suite():
    """Ran test suite."""
    loader = unittest.TestLoader()
    test_suite = loader.discover('test/models', '*_test.py')
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    cov = coverage.Coverage()
    cov.start()
    runner.run(suite())
    cov.stop()
    cov.save()

    cov.html_report()
