#!/usr/bin/python3
"""Main file with Handler class."""
from time import sleep
from esc import ESCEmulator

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

interval = 5  # sleep interval


def main():
    """
    Do main loop.
    Returns
    -------
    None.
    """
    _id = "id"
    bike = ESCEmulator(_id)
    finished = False
    while not finished:
        sleep(interval)
        res = bike.ride_bike()
        finished = res['finished']
    print('Quitting esc simulator!')
    if res['destination_reached']:
        print('... and destination reached :)')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
