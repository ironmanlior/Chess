#!/usr/bin/python
from enum import Enum

class Status(Enum):
    check = 0
    mate = 1
    pate = 2
    draw = 3
    time_up = 4
    repetition = 5
    resign = 6
    null = 7