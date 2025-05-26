from kivy.lang import Builder

from .Chat import *
from .Moves import *
from .UserInfo import *
from ...Popup.Verify import *

Builder.load_file("./App/Pages/Game/game.kv")
Builder.load_file("./App/Pages/Game/menu.kv")

from .game import *
from .menu import *
from . import game
from . import menu