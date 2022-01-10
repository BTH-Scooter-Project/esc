#!/usr/bin/python3
"""Main file with Handler class."""

import json
from time import time, sleep
from pprint import pprint
from pathlib import Path
import requests
from colorama import Fore, Back
from api import Api
from esc import ESCEmulator

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

CONFIG_FILE = 'config/config.json'
start_bike_id = 201
test = False
if not Path(CONFIG_FILE).exists():
    test = True
SIMULATION_ACCELERATION = 10
TEXT_COLOR_AFTER = Fore.RESET + Back.RESET
TEXT_GREEN = Fore.BLACK + Back.GREEN
TEXT_COLOR = Fore.BLACK + Back.YELLOW
MAIN_TEXT_COLOR = Fore.BLACK + Back.RED


def get_config(file):
    """Load config settings."""
    if test:
        file = f'test/{file}'
    with open(file, 'r') as file_handle:
        return json.load(file_handle)


def get_system_mode(config_file):
    """Fetch system mode (simulation or not)."""
    config = get_config(config_file)
    system_mode_url = config['BASE_URL'] + '/v1/bike/mode?apiKey=' + config['API_KEY']
    res_data = requests.get(system_mode_url).json()['data']
    if test:
        res_data['nr_of_bikes'] = 1
    pprint(res_data)
    return res_data


def simulate_bike_rides(bikes, accum_processing_time, sleep_interval):
    """Simulate bike rides."""
    bikes_to_be_removed = []

    for bike in bikes:
        start_time = time()
        res = bike.ride_bike()
        passed_time = time() - start_time
        if res['finished'] or res['canceled']:
            print('Quitting esc program!')
            if res['destination_reached']:
                print('... and destination reached')
            bikes_to_be_removed.append(bike)
        sleep_time = (sleep_interval - passed_time) if passed_time < sleep_interval else 0
        accum_processing_time = accum_processing_time + max(passed_time, sleep_interval)
        lag_time = 0
        if passed_time > sleep_interval:
            lag_time = passed_time - sleep_interval
            print(TEXT_COLOR + f'(ESC program) System lagging: {lag_time}' + TEXT_COLOR_AFTER)
        sleep(sleep_time)
    return (bikes_to_be_removed, accum_processing_time)


def esc_main():
    """Do main loop.

    Returns
    -------
        None
    """
    data = get_system_mode(CONFIG_FILE)
    path = ''
    if test:
        path = 'test/'
    api = Api(relative_path=path)
    if test:
        api.rent_bike(1)
    # sleep_interval = data['interval'] / (data['nr_of_bikes'] + 1)
    start_rent_time = time()
    if data['simulation']:
        end_bike_id = start_bike_id + data['nr_of_bikes']
        for bike_id in range(start_bike_id, end_bike_id):
            api.rent_bike_without_token(bike_id)
    rent_time = time() - start_rent_time
    accum_processing_time = 0
    total_lag = 0
    generation_time = 0
    bikes = []
    show_stat = True
    while True:
        rented_bike_ids = api.get_rented_bikes()
        start_generation_time = time()
        for bike_id in rented_bike_ids:
            bikes.append(ESCEmulator(bike_id, data['interval'] * SIMULATION_ACCELERATION, test=test))
        generation_time = max(generation_time, time() - start_generation_time)
        sleep_interval = data['interval'] / (len(bikes) + 1)
        (bikes_to_be_removed, accum_processing_time) = simulate_bike_rides(bikes, accum_processing_time, sleep_interval)
        for bike in bikes_to_be_removed:
            bikes.remove(bike)
        bikes_to_be_removed = []
        sleep_time = (data['interval'] - accum_processing_time) if accum_processing_time < data['interval'] else 0
        if accum_processing_time > data['interval']:
            lag_time = accum_processing_time - data['interval']
            print(MAIN_TEXT_COLOR + f'(main) System lagging: {lag_time}' + TEXT_COLOR_AFTER)
            total_lag = total_lag + lag_time
        accum_processing_time = 0
        sleep(sleep_time)
        if show_stat and len(bikes) == 0:
            print(TEXT_GREEN + f'Rent time: {rent_time}' + TEXT_COLOR_AFTER)
            print(TEXT_GREEN + f'Maximal esc generation time: {generation_time}' + TEXT_COLOR_AFTER)
            print(MAIN_TEXT_COLOR + f'Total system lagging: {total_lag}' + TEXT_COLOR_AFTER)
            print('Total simulation time:', time() - start_rent_time)
            total_lag = 0
            show_stat = False
            if test:
                return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    esc_main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
