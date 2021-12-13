#!/usr/bin/python3
"""Main file with Handler class."""
from api import Api

bike_id = 7


def main():
    api = Api()
    api.rent_bike(bike_id)
    api.get_rented_bikes()
    api.get_states_for_all_bikes()


if __name__ == '__main__':
    main()
