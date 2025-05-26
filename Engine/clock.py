#!/usr/bin/python
from .Enum import Color
import time
from datetime import datetime, timedelta


class Clock(object):
    def __init__(self, color: Color, game_time: timedelta, start_time: datetime):
        self.game_time = game_time
        self.start_time = start_time
        self.color = color
        self.running = bool(color.value)
        self.update(start_time)
    
    def stop(self, now: datetime):
        self.game_time -= now - self.start_time
        self.running = False
        
    def start(self, now: datetime):
        self.start_time = now
        self.running = True

    def update(self, now: datetime):
        if self.running:
            time_past = now - self.start_time
            self.start_time = now
            self.game_time -= time_past
    
    def __str__(self):
        self.time_left = ":".join(f"{self.game_time}".split(":")[1:])
        if self.game_time >= timedelta(seconds=10):
            self.time_left = self.time_left.split(".")[0]
        return self.time_left

class ChessClock(object):
    def __init__(self, game_time: timedelta):
        self.game_time: timedelta = game_time
        now = datetime.now()
        self.clocks_dict = {color: Clock(color, self.game_time, now) for color in Color}
        self.clocks = [self.clocks_dict[Color.white], self.clocks_dict[Color.black]]
        self.update()
    
    def __getitem__(self, color: Color):
        return self.clocks_dict[color]
    
    def swich(self):
        now = datetime.now()
        self.clocks[0].stop(now)
        self.clocks[1].start(now)
        self.clocks.reverse()
    
    def update(self):
        now = datetime.now()
        try:
            self.clocks
        except AttributeError:
            return
        self.clocks[0].update(now)
        if self.clocks[0].game_time.total_seconds() <= 0:
            raise TimeoutError(f"{self.clocks[0].color.name}")