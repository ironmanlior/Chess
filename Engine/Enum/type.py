#!/usr/bin/python
from enum import Enum

class PieceType(Enum):
    pawn = [1, 1, 0] # 6
    knight = [1, 0, 1] # 5
    bishop = [1, 0, 0] # 4
    rook = [0, 1, 1] # 3
    queen = [0, 1, 0] # 2
    king = [0, 0, 1] # 1
    joker = [0, 0, 0]
    null = [0, 0, 0, 0]