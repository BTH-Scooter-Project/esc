"""Customer class."""
# models.py

import json
# from pprint import pprint
from pathlib import Path
import requests
from flask_login import UserMixin, current_user


def set_config_file(dev_config_file, test_config_file='test/config/config.json'):
    """Choose either dev or test config file."""
    config_file = test_config_file
    if Path(dev_config_file).exists():
        config_file = dev_config_file
    return config_file


class Customer(UserMixin):
    """Customer class.

    Args
    ----
        UserMixin ([type]): [description]
        db ([type]): [description]
    """

    CONFIG_FILE = set_config_file('project/static/config/config.json')
    customers = []

    def __init__(self, _id, token, email):
        """Init."""
        self.id = _id
        self.token = token
        self.email = email
        self.get_customer_info()
        self.set_customer(self)

    @classmethod
    def set_customer(cls, self):
        """Add customer to the class."""
        cls.customers = []
        cls.customers.append(self)
        # print('cls.customers.id(cls.set_customer): ' + cls.customers[0].get_id())
        # print("len(cls.customers)", len(cls.customers))

    def get_id(self):
        """Get customer id."""
        return str(self.id)

    @classmethod
    def get_customer_by_id(cls, user_id):
        """Get customer by id."""
        if cls.customers and cls.customers[0].get_id() == user_id:
            return cls.customers[0]
        return None

    @staticmethod
    def get_config(file):
        """Read config file.

        This file should be protected (attached at runtime by docker-compose)

        Args
        ----
            file (string): File path relative to the current position
        Returns
        -------
            dict: Dictionary containing config
        """
        with open(file, mode='r', encoding="utf8") as file_handle:
            return json.load(file_handle)

    @staticmethod
    def login(email, password=None, unique_id=None):
        """Login request implementation.

        Args
        ----
            email (str): email address
            password (str): plain text password
        Returns
        -------
            (int, str): Touple: customerId and JWT token
        """
        config = Customer.get_config(Customer.CONFIG_FILE)
        login_url = config['BASE_URL'] +\
            '/v1/auth/customer/login?apiKey=' + config['API_KEY']
        login_obj = {
            'email': email,
            # 'password': password,
            'unique_id': unique_id
        }
        if password is not None and password != '':
            login_obj['password'] = password
        req = requests.post(
            login_url,
            data=login_obj
        )
        if req.status_code == 200:
            login_obj = req.json()['data']
            login_obj['status_code'] = req.status_code
            # customer = Customer(login_obj['id'], login_obj['token'], email)
            # pprint(login_obj)
            # print("customer_id(login)", login_obj['id'])
            return login_obj

        error_obj = req.json()['errors']
        error_obj['status_code'] = req.status_code
        if not hasattr(error_obj, 'message'):
            error_obj['message'] = error_obj['title']
        # print("login error")
        # pprint(error_obj)

        return error_obj

    @staticmethod
    def get(customer_id):
        """Get customer by customer id and jwt.

        Args
        ----
            customer_id (int): Customer id
            jwt (str): JSON Web Token
        Returns
        -------
            Customer: Either customer object or None if not found
        """
        # if customer_id is the same and customer object exists (customers list not empty)
        if current_user.id == customer_id and not Customer.customers:
            return Customer.customers[0]
        return None

    def get_customer_info(self):
        """Get info about the customer.

        Args
        ----
            customer_id (int)

        Returns
        -------
            dict: customer_info
        """
        # customer_info = self.get(self.id, self.token)
        config = self.get_config(self.CONFIG_FILE)
        customer_info_url = config['BASE_URL'] + f'/v1/auth/customer/{self.id}?apiKey=' + config['API_KEY']
        headers = {
            'x-access-token': self.token,
        }
        req = requests.get(
            customer_info_url,
            headers=headers
        )

        response = req.json()
        # print("get_customer_info: ", response)
        customer_info = response['data']

        self.firstname = customer_info['firstname']
        self.lastname = customer_info['lastname']
        self.cityid = customer_info['cityid']
        self.payment = customer_info['payment']
        self.balance = customer_info['balance']

        return self

    @staticmethod
    def register(email, password, firstname, lastname, city_id, unique_id=-1):
        """Register new customer.

        Args
        ----
            email (str): Email address
            password (str): Plaintext password
            firstname (str): Firstname
            lastname (str): Lastname
            city_id (int): City id matching id in the city table
        Returns
        -------
            None
        """
        config = Customer.get_config(Customer.CONFIG_FILE)
        register_customer_url = config['BASE_URL'] + '/v1/auth/customer?apiKey=' + config['API_KEY']

        body_obj = {
            "email": email,
            "password": password,
            "firstname": firstname,
            "lastname": lastname,
            "cityid": city_id
        }
        if unique_id != -1:
            body_obj['unique_id'] = unique_id
        req = requests.post(
            register_customer_url,
            data=body_obj
        )
        if req.status_code == 201:
            customer_info = req.json()['data']
            customer_info['email'] = email
            customer_info['password'] = password
            customer_info['status_code'] = req.status_code
            # pprint(customer_info)
            return customer_info

        if req.status_code == 200:
            customer_info = req.json()['data']
            customer_info['email'] = customer_info['user']
            customer_info['status_code'] = req.status_code
            customer_info['detail'] = ''
            # pprint(customer_info)
            return customer_info

        # print(req)
        error_obj = req.json()['errors']
        error_obj['status_code'] = req.status_code
        return error_obj

    def update(self, email, balance, payment, password):
        """Fetch and update customer info.

        Args
        ----
            payment (str): prepaid or card
            balance (int): Set new balance
            password (str): Password (if empty = no change)

        Returns
        -------
            None
        """
        config = Customer.get_config(Customer.CONFIG_FILE)
        update_url = config['BASE_URL'] + '/v1/auth/customer?apiKey=' + config['API_KEY']
        body_obj = {
            "email": email,
            "password": password,
            "balance": balance,
            "payment": payment,
        }
        headers = {
            'x-access-token': self.token,
        }
        req = requests.put(
            update_url,
            data=body_obj,
            headers=headers
        )
        if req.status_code == 200:
            self.balance = balance
            self.payment = payment
            customer_info = req.json()['data']
            customer_info['status_code'] = req.status_code
            # pprint(customer_info)
            return customer_info

        error_obj = req.json()['errors']
        error_obj['status_code'] = req.status_code
        return error_obj

    def get_travel_info(self):
        """Get customers travelinfo.

        Args
        ----
            None
        Returns
        -------
            list(dict): travel_info
        """
        config = self.get_config(self.CONFIG_FILE)
        travel_info_url = config['BASE_URL'] + f'/v1/travel/customer/{self.id}?apiKey=' + config['API_KEY']
        headers = {
            'x-access-token': self.token,
        }
        req = requests.get(
            travel_info_url,
            headers=headers
        )

        response = req.json()
        # print(response)
        travel_info = response['data']

        return travel_info
