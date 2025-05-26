from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.graphics import Color
from Engine.board import Board
from .....session import session

class PlaceLayout(Button):
    id_x = NumericProperty()
    id_y = NumericProperty()
    source = StringProperty()
    
    
    def update(self):
        try:
            board: Board = session["game"].board
            place = board[self.id_y][self.id_x]
            self.source = "" if place.is_empty() else place.piece.img
            b = 1
            self.background_color = (0, 0, 0, 0)
            if board.selected:
                if (self.id_x, self.id_y) == board.selected.pos:
                    self.background_color = (.75, 0, 0, .5)
                elif (self.id_x, self.id_y) in board.selected.moves:
                    self.background_color = (.75, .75, 0, .5)
                else:
                    b = 0
            else:
                b = 0

            if self.source != "":
                b = 1
            with self.canvas:
                for color in self.canvas.before.children:
                    if isinstance(color, Color):
                        color.a = int(self.source != "")
                self.canvas.opacity = b
        except Exception as e:
            pass
        
