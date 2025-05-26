#!/usr/bin/python

from DB import User
from datetime import datetime
from Compression import Compress, Decompress

class Message(object):
    def __init__(self, message, sender: User, receiver: User):
        self.freq = {}
        self.message = message
        self.sender = sender
        self.receiver = receiver
        self.time = datetime.now()
    
    @property
    def message(self):
        @Decompress
        def inner():
            return self.__message, self.freq
        return inner()

    @message.setter
    def message(self, value):
        @Compress
        def inner(value, freq):
            return value, freq
        self.__message, self.freq = inner(value)
        
    def __str__(self):
        return f"{Decompress(self.__message)}"