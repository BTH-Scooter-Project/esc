#!/usr/bin/python3
""" For testing """

values = ["a", "b", "c"]

for ix, value in enumerate(values):
    print(ix)
    if ix == 1:
        break
print(ix)
