#!/usr/bin/python

class MetaBoard(type):
    def __init__(cls, *args, **kwargs):
        cls.positions = [(j, i) for j in range(8) for i in range(8)]
    
    def __call__(cls, *args, **kwargs):
        self = cls.__new__(cls, *args, **kwargs)
        return self