import requests
import json


class Api:
    """Define api class for working with api"""
    CONFIG_FILE = 'config/config.json'

    def __init__(self):
        self.config = self.get_config(self.CONFIG_FILE)
        self.token = None

        self.login()

    @staticmethod
    def get_config(file):
        with open(file, 'r') as file_handle:
            return json.load(file_handle)

    def login(self):
        login_url = self.config['BASE_URL'] + '/v1/auth/customer/login?apiKey=' + self.config['API_KEY']
        login_obj = {
            'email': self.config['email'],
            'password': self.config['password'],
        }
        req = requests.post(
            login_url,
            data=login_obj
        )
        res_json = req.json()
        self.token = res_json['data']['token']
        print("res_json", res_json)

    def rent_bike(self, bike_id):
        rent_url = self.config['BASE_URL'] + f'/v1/travel/bike/{bike_id}?apiKey=' + self.config['API_KEY']
        headers_obj = {
            'x-access-token': self.token,
        }
        req = requests.post(
            rent_url,
            headers=headers_obj
        )
        res_json = req.json()
        print(res_json)

    def get_rented_bikes(self):
        rent_url = self.config['BASE_URL'] + '/v1/travel/rented?apiKey=' + self.config['API_KEY']
        req = requests.get(rent_url)
        res_json = req.json()
        print(res_json)


# print(x.status_code)

