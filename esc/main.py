#!/usr/bin/python3
"""Main file with Handler class."""
from time import sleep
from esc import ESCEmulator

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

interval = 5  # sleep interval


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


def main():
    """
    Do main loop.
    Returns
    -------
    None.
    """
    esc_properties = dict(
            id="id",
            battery_capacity=10000,  # in seconds
            max_speed=40  # max speed in km/h
        )
    esc_state = dict(
        battery_level=1000,  # battery level in seconds
        current_position=[59.347561, 18.025832],  # gps coordinates of the current position
        locked=False  # Boolean
    )
    system_properties = dict(
        destination=[59.324783, 18.073070],  # gps coordinates of the destination (finish) position
        sleep_time=interval*10,  # in seconds
        travel_points=4,  # number of travel gps-coordinates along the path
        allowed_area=[[59.351495, 18.023087], [59.305341, 18.168215]]  # Boolean
    )
    bike = ESCEmulator(esc_properties, esc_state, system_properties)
    finished = False
    while not finished:
        sleep(interval)
        finished = bike.ride_bike()
    print('Quitting esc simulator!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
