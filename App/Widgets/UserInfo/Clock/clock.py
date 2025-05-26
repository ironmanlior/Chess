from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from Engine import Color, ChessClock, Game
from .....session import session

class GameClock(MDBoxLayout):
    clock = ObjectProperty()
    color = StringProperty()
    text = StringProperty()
    icon = StringProperty()
    
    def start(self):
        global session
        self.icons = [
            "clock-time-one-outline", 
            "clock-time-two-outline", 
            "clock-time-three-outline", 
            "clock-time-four-outline", 
            "clock-time-five-outline", 
            "clock-time-six-outline",
            "clock-time-seven-outline",
            "clock-time-eight-outline",
            "clock-time-nine-outline",
            "clock-time-ten-outline",
            "clock-time-eleven-outline",
            "clock-time-twelve-outline"
        ]
        self.icons_iter = iter(self.icons)
        self.text = "00:00"
        self.icon = ""
        self.clock = None
        color: Color = session.get("color", Color.white)
        self.color = color.name
        try:
            game: Game = session.get("game", None)
            self.clock: ChessClock = game.clock if game and game.clock else None
            self.text = f"{self.clock[Color[self.color]]}" if self.clock else "00:00"
            self.icon = next(self.icons_iter) if self.clock and self.clock[Color[self.color]].running else ""
        except Exception as e:
            pass
        Clock.schedule_interval(lambda x: self.update(), 1/120)
    
    def update(self):
        global session
        try:
            game: Game = session.get("game", None)
            self.clock: ChessClock = game.clock if game and game.clock else None
            self.icon = next(self.icons_iter) if self.clock and self.clock[Color[self.color]].running else ""
            self.clock.update()
            self.text = f"{self.clock[Color[self.color]]}" if self.clock else "00:00"
        except StopIteration as e:
            self.icons_iter = iter(self.icons)
        except TimeoutError as e:
            return False
        except Exception as e:
            self.text = "00:00"
            return False
