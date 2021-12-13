import requests, json, pprint


class Api:
    """Define api class for working with api"""
    CONFIG_FILE = '../config/config.json'

    def __init__(self, bike_id=-1):
        self.config = self.get_config(self.CONFIG_FILE)
        self.token = None
        self.rented_bike_ids = []

        self.login()
        if bike_id != -1:
            self.rent_bike(bike_id)
            self.get_rented_bikes()
            self.bike_state = self.get_bike_state(bike_id)

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
        self.rented_bike_ids = req.json()
        print(self.rented_bike_ids)

    def get_bike_state(self, bike_id):
        state_url = self.config['BASE_URL'] + f'/v1/bike/{bike_id}?apiKey=' + self.config['API_KEY']
        req = requests.get(state_url)
        bike_state = req.json()['data']
        pprint.pprint(bike_state)
        return bike_state

    def get_states_for_all_bikes(self):
        for bike_id in self.rented_bike_ids:
            self.get_bike_state(bike_id)

# print(x.status_code)
