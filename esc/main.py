#!/usr/bin/python3
"""Main file with Handler class."""
import json
import requests
from time import time, sleep
from esc import ESCEmulator
from pprint import pprint
from api import Api

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

start_bike_id = 101
CONFIG_FILE = 'config/config.json'
simulation_acceleration = 10


def get_config(file):
    with open(file, 'r') as file_handle:
        return json.load(file_handle)


def get_system_mode(config_file):
    config = get_config(config_file)
    system_mode_url = config['BASE_URL'] + '/v1/bike/mode?apiKey=' + config['API_KEY']
    res_data = requests.get(system_mode_url).json()['data']
    pprint(res_data)
    return res_data


def main():
    """
    Do main loop.
    Returns
    -------
    None.
    """
    data = get_system_mode(CONFIG_FILE)
    api = Api()
    sleep_interval = data['interval'] / (data['nr_of_bikes'] + 1)
    if data['simulation']:
        end_bike_id = start_bike_id + data['nr_of_bikes']
        for bike_id in range(start_bike_id, end_bike_id):
            api.rent_bike_without_token(bike_id)
    accumulated_sleep_time = 0
    res = None
    bikes = []
    bikes_to_be_removed = []
    while True:
        rented_bike_ids = api.get_rented_bikes()
        for bike_id in rented_bike_ids:
            bikes.append(ESCEmulator(bike_id, data['interval'] * simulation_acceleration))
        for bike in bikes:
            start_time = time()
            res = bike.ride_bike()
            passed_time = start_time - time()
            if res['finished'] or res['canceled']:
                print('Quitting esc program!')
                if res['destination_reached']:
                    print('... and destination reached')
                bikes_to_be_removed.append(bike)
            sleep_time = (sleep_interval - passed_time) if passed_time <= sleep_interval else 0
            accumulated_sleep_time = accumulated_sleep_time + sleep_time
            if sleep_time == 0:
                lag_time = sleep_interval - passed_time
                print(f'System lagging (esc program): {lag_time}')
            sleep(sleep_time)
        for bike in bikes_to_be_removed:
            bikes.remove(bike)
        bikes_to_be_removed = []
        sleep_time = (data['interval'] - accumulated_sleep_time) if accumulated_sleep_time <= data['interval'] else 0
        if sleep_time == 0:
            lag_time = data['interval'] - accumulated_sleep_time
            print(f'System lagging (main): {lag_time}')
        accumulated_sleep_time = 0
        sleep(sleep_time)
        sleep_interval = data['interval'] / (len(bikes) + 1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
