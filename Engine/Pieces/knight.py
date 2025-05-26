#!/usr/bin/python

from .Base import Piece, MetaPiece, Place
from ..Enum import PieceType, Color

class Knight(Piece, metaclass = MetaPiece):
    """
    Description:
        Knight is a Piece in Chess.
        Each player get two Knights in his/her side.
        The Knight can move two steps in one direction and then move one step in 90 degrees relative to the first direction.
        The Knight can move thought other pieces.
    
    Args:
        Piece (type): Knight inherits from Piece
        metaclass (MetaPiece, optional): the meta class is MetaPiece. Defaults to MetaPiece.

    Returns:
        Knight: Knight object
    """
    
    def __init__(self, color: Color, id):
        super().__init__(PieceType.knight, 3, (1 + 5 * id, 7 * color.value), color, id)
    
    def get_rules(self, positions):
        super().get_rules(positions)
        self.rules.extend([[pos1] if (pos1 := (self.x + j, self.y + i)) in positions else [] for j in [-2, 2] for i in [-1, 1]])
        self.rules.extend([[pos1] if (pos1 := (self.x + j, self.y + i)) in positions else [] for j in [-1, 1] for i in [-2, 2]])
    
    @Piece.check_pos
    def valid_moves(self, board: list[list[Place]], moves: list[list[tuple]]):
        check_moves = []
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                pos = moves[i][j]
                place = board[pos[1]][pos[0]]
                place.protect(self.color)
                if not place.empty:
                    if place.piece.color == self.color:
                        moves[i].clear()
                    else:
                        if place.piece.king:
                            check_moves.append(self.pos)
        return check_moves