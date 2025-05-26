from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from Engine import Color, Status, Game
from DB import User
from ...session import session

class GamePage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "game"
        self.end_game: MDDialog = None
        self.verify: MDDialog = None
    
    def on_enter(self):
        global session
        self.rival = session["rival"]
        self.user = session["user"]
        self.user_color = session["color"].name
        self.rival_color = Color(1 - Color[self.user_color].value).name
        
        self.ids.user_info.update(self.user, self.user_color)
        self.ids.rival_info.update(self.rival, self.rival_color)
        self.ids.board.start(self.add_move, self.open_end_game)
        self.ids.moves.game_update = self.ids.board.update
        self.ids.chat.ids.chat_history.start()
    
    def add_move(self):
        self.ids.moves.ids.history.add_move()
    
    def open_end_game(self, winner):
        global session
        game: Game = session["game"]
        user: User = session["user"]
        rival: User = session["rival"]
        score: float = .5 if game.status in [Status.draw, Status.repetition, Status.pate] else 1.
        e_score: float = 1 / (1 + 10 ** ((rival.rating - user.rating) / 400))
        winner = session["client"].recv()
        title = game.status.name
    
    def spinner_clicked(self, value):
        self.type = value


class EndGame(MDBoxLayout):
    def __init__(self):
        pass