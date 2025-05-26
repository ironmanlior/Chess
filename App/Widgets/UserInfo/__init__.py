from kivy.lang import Builder

from . import Clock
from .Clock import Clock

Builder.load_file("./App/Pages/Game/UserInfo/user_info.kv")

from . import user_info
from .user_info import UserInfo