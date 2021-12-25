#!/usr/bin/python3
"""Main file with Handler class."""
import json
import requests
from time import time, sleep
from esc import ESCEmulator
from pprint import pprint
from api import Api
from colorama import Fore, Back

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

start_bike_id = 201
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
    res = None
    bikes = []
    bikes_to_be_removed = []
    text_color_after = Fore.RESET + Back.RESET
    text_color = Fore.BLACK + Back.YELLOW
    text_green = Fore.BLACK + Back.GREEN
    main_text_color = Fore.BLACK + Back.RED
    show_stat = True
    while True:
        rented_bike_ids = api.get_rented_bikes()
        start_generation_time = time()
        for bike_id in rented_bike_ids:
            bikes.append(ESCEmulator(bike_id, data['interval'] * simulation_acceleration))
        generation_time = max(generation_time, time() - start_generation_time)
        sleep_interval = data['interval'] / (len(bikes) + 1)
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
                print(text_color + f'(ESC program) System lagging: {lag_time}' + text_color_after)
            sleep(sleep_time)
        for bike in bikes_to_be_removed:
            bikes.remove(bike)
        bikes_to_be_removed = []
        sleep_time = (data['interval'] - accum_processing_time) if accum_processing_time < data['interval'] else 0
        if accum_processing_time > data['interval']:
            lag_time = accum_processing_time - data['interval']
            print(main_text_color + f'(main) System lagging: {lag_time}' + text_color_after)
            total_lag = total_lag + lag_time
        accum_processing_time = 0
        sleep(sleep_time)
        if show_stat and len(bikes) == 0:
            print(text_green + f'Rent time: {rent_time}' + text_color_after)
            print(text_green + f'Maximal esc generation time: {generation_time}' + text_color_after)
            print(main_text_color + f'Total system lagging: {total_lag}' + text_color_after)
            total_lag = 0
            show_stat = False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
