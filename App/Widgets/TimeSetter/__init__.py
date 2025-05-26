from kivy.lang import Builder

Builder.load_file("./App/Widgets/TimeSetter/time_setter.kv")

from . import time_setter
from .time_setter import GameTime