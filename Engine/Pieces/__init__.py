#!/usr/bin/python

from .Base import MetaPiece, Piece
from .king import King
from .queen import Queen
from .rook import Rook
from .bishop import Bishop
from .knight import Knight
from .pawn import Pawn
from ..Enum import PieceType, Color
from copy import deepcopy

class Pieces(object):
    def __init__(self):
        self.pieces: dict[Color, dict[PieceType, list[Piece]]] = {color: {key: [] for key in MetaPiece.Pieces} for color in Color}
        self.limit = {
            PieceType.king: {color: 1 for color in Color},
            PieceType.queen: {color: 1 for color in Color},
            PieceType.rook: {color: 2 for color in Color},
            PieceType.bishop: {color: 2 for color in Color},
            PieceType.knight: {color: 2 for color in Color},
            PieceType.pawn: {color: 8 for color in Color}
        }
     
    def __deepcopy__(self, memo={}):
        copy = super().__new__(type(self)) # create new piece of the same type
        memo[id(self)] = self
        for k, v in vars(self).items():
            setattr(copy, k, deepcopy(v, memo))
        return copy # return the copy piece
    
    def __getitem__(self, key):
        try:
            return self.pieces[key]
        except KeyError:
            return None
    
    def __iter__(self):
        return iter(self.pieces)
    
    def add(self, piece: Piece) -> None:
        self.pieces[piece.color][piece.name].append(piece)
        self.limit[piece.name][piece.color] += 1
    
    def create(self, piece_type: PieceType, color: Color) -> Piece:
        piece = MetaPiece.Pieces[piece_type](color, len(self.pieces[color][piece_type]))
        self.pieces[color][piece_type].append(piece)
        return piece
    
    def delete(self, piece: Piece) -> None:
        if piece in self.pieces[piece.color][piece.name]:
            self.pieces[piece.color][piece.name].remove(piece)
