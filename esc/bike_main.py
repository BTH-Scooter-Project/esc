#!/usr/bin/python3
"""Main esc-program file."""

import sys
from time import sleep
from esc import ESCEmulator

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    """
    Do main loop.
    Returns
    -------
    None.
    """
    args = sys.argv[1:]
    print(f'args: {args}')
    bike_id = int(args[0])
    interval = int(args[1])
    bike = ESCEmulator(bike_id, interval)
    finished = False
    res = None
    while not finished:
        sleep(interval)
        res = bike.ride_bike()
        finished = res['finished']
    print('Quitting esc program!')
    if res['destination_reached']:
        print('... and destination reached :)')
    exit(0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
