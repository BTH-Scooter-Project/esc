"""Main module for the API communication."""

import json
# from pprint import pprint
import requests


class Api:
    """Define api class for working with api."""

    CONFIG_FILE = 'config/config.json'

    def __init__(self, bike_id=-1):
        """Init setting from config-file."""
        self.config = self.get_config(self.CONFIG_FILE)
        self.token = None
        self.rented_bike_ids = []

        # self.login()
        if bike_id != -1:
            # self.rent_bike(bike_id)
            # self.rent_bike_without_token(bike_id)
            # self.get_rented_bikes()
            self.bike_state = self.get_bike_state(bike_id)

    @staticmethod
    def get_config(file):
        """Fetch config."""
        with open(file, 'r') as file_handle:
            return json.load(file_handle)

    def login(self):
        """Login."""
        login_url = self.config['BASE_URL'] + '/v1/auth/customer/login?apiKey=' + self.config['API_KEY']
        login_obj = {
            'email': self.config['email'],
            'password': self.config['password'],
        }
        req = requests.post(
            login_url,
            data=login_obj
        )
        login_json = req.json()['data']
        self.token = login_json['token']
        # print("login msg")
        # pprint(login_json)

    def rent_bike(self, bike_id):
        """Rent bike."""
        rent_url = self.config['BASE_URL'] + f'/v1/travel/bike/{bike_id}?apiKey=' + self.config['API_KEY']
        headers_obj = {
            'x-access-token': self.token,
        }
        # req =
        requests.post(
            rent_url,
            headers=headers_obj
        )
        # req_json = req.json()
        # bike_json = req.json()['data']
        # pprint(bike_json)
        # print("bike state:")
        # pprint(req_json)

    def rent_bike_without_token(self, bike_id):
        """Rent bike without token (simulator)."""
        rent_url = self.config['BASE_URL'] + '/v1/travel/simulation?apiKey=' + self.config['API_KEY']
        rent_obj = {
            'customerid': f'{bike_id}',
            'bikeid': f'{bike_id}',
        }
        # req =
        requests.post(
            rent_url,
            data=rent_obj
        )
        # req_json = req.json()
        # bike_json = req.json()['data']
        # pprint(bike_json)
        # print("bike state:")
        # pprint(req_json)

    def get_rented_bikes(self):
        """Fetch list with rented bikes."""
        rent_url = self.config['BASE_URL'] + '/v1/travel/rented?apiKey=' + self.config['API_KEY']
        req = requests.get(rent_url)
        self.rented_bike_ids = req.json()
        # print(self.rented_bike_ids)
        return self.rented_bike_ids

    def get_bike_state(self, bike_id):
        """Fetch bike state."""
        state_url = self.config['BASE_URL'] + f'/v1/bike/{bike_id}?apiKey=' + self.config['API_KEY']
        req = requests.get(state_url)
        bike_state = req.json()['data']
        # pprint(bike_state)
        return bike_state

    def get_states_for_all_bikes(self):
        """Get states for all bikes."""
        for bike_id in self.rented_bike_ids:
            self.get_bike_state(bike_id)
