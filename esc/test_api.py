#!/usr/bin/python3
"""Main file with Handler class."""
from api import Api

bike_id = 3


def main():
    api = Api()
    api.rent_bike(bike_id)
    api.get_rented_bikes()


if __name__ == '__main__':
    main()
