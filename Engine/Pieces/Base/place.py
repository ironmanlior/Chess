from __future__ import annotations
from .piece import Piece
from ...Enum.color import Color

class Place(object):
    def __init__(self, x, y):
        self.pos = self.x, self.y = (x, y)
        self.piece: Piece = None
        self.protected: dict[Color, bool] = {color: False for color in Color}
        self.empty = True
    
    def __hash__(self):
        return hash(self.piece)
    
    def __eq__(self, other: Place):
        return self.piece == other.piece and self.protected == other.protected
    
    def __getitem__(self, index):
        return self.pos[index % len(self.pos)]
    
    def kill(self):
        try:
            self.piece.kill()
        except Exception as e:
            pass
        self.clear()
    
    def push(self, piece: Piece):
        self.kill()
        try:
            piece.move(self.pos)
        except Exception as e:
            pass
        self.piece = piece
        self.empty = self.is_empty()
    
    def replace(self, other: Place):
        piece = self.piece
        self.push(other.piece)
        try:
            self.piece.first = False
        except Exception as e:
            pass
        other.clear()
        return piece
    
    def select(self):
        self.piece.select()
    
    def protect(self, color: Color):
        self.protected[color] = True
    
    def unprotect(self):
        self.protected = {color: False for color in Color}
    
    def is_protected(self, color: Color):
        return self.protected[color]
    
    def clear(self):
        self.piece = None
        self.empty = True
        self.protected = {color: False for color in Color}
    
    def is_empty(self):
        return self.piece == None
    
    def __str__(self):
        return f"{self.pos}"