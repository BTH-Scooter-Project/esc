#!/usr/bin/python3
"""Main file with Handler class."""
from time import sleep

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

interval = 10  # sleep interval


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


def main(tree):
    """
    Do main loop.
    Returns
    -------
    None.
    """
    finished = False
    while not finished:
        inp = show_menu()
        res = process_choice(inp, tree)
        if res:
            finished = True
        sleep(interval)
    print('Quitting esc simulator!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
