from kivy.lang import Builder
from .Place import *
Builder.load_file("./App/Pages/Game/Board/board.kv")

from .Place import PlaceLayout
from .board import BoardLayout