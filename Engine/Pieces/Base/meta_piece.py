from ...Enum import PieceType
from .piece import Piece

class MetaPiece(type):
    Pieces = {}
    def __new__(cls, name: str, bases: tuple[type, ], namespace, **kwargs):
        if Piece in bases:
            new = super().__new__(cls, name, bases, namespace, **kwargs)
            MetaPiece.Pieces[PieceType[name.lower()]] = new
            Piece.types[PieceType[name.lower()]] = new
        else:
            new = type(name, bases, namespace)
        return new

