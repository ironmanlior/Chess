from kivymd.uix.gridlayout import MDGridLayout
from kivy.clock import Clock
from .Place import PlaceLayout
from Engine import Game, Color
from App.session import session
import select

class BoardLayout(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 8
        self.rows = 8
    
    def start(self, add_move, open_end_game):
        self.add_move = add_move
        self.open_end_game = open_end_game
        
        color: Color = session["color"]
        for y in range(8):
            for x in range(8):
                if not color.value:
                    x, y = 7 - x, 7 - y
                place = PlaceLayout(id_x=x, id_y=y)
                self.add_widget(place)
                place.update()
        if not color.value:
            Clock.schedule_interval(lambda x: self.get_game(), 0.05)
    
    def update(self):
        for place in self.children:
            place: PlaceLayout = place
            place.update()
    
    def rotate(self):
        for place in self.children:
            place: PlaceLayout = place
            place.id_x, place.id_y = 7 - place.id_x, 7 - place.id_y
            place.update()
    
    def on_press(self, widget: PlaceLayout):
        widget.background_color = (0, .25, .75, .5)
    
    def get_game(self):
        global session
        for socket in select.select([session["client"].client], [], [], .001)[0]:
            recv = socket.recv()
            if type(recv) == Game:
                session["game"] = recv
                winner = session["game"].Status()
                self.add_move()
                self.update()
                if winner:
                    self.open_end_game(winner)
            return False
    
    def on_release(self, widget: PlaceLayout):
        global session
        game: Game = session["game"]
        color: Color = session["color"]
        x, y = widget.id_x, widget.id_y
        widget.background_color = (0, 0, 0, 0)
        if color == game.current[0]:
            if not game.is_selected():
                try:
                    game.select(game.board[y][x])
                except Exception as e:
                    pass
            else:
                try:
                    game.move((x, y))
                    session["client"].send(game)
                    winner = game.Status()
                    self.add_move()
                    if winner:
                        self.update()
                        self.open_end_game(winner)
                        return
                    Clock.schedule_interval(lambda x: self.get_game(), .05)
                except Exception as e:
                    try:
                        game.board.selected.select()
                        game.board.selected = None
                    except Exception as e:
                        pass
        self.update()
