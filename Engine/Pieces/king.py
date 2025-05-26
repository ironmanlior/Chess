#!/usr/bin/python

from .Base import Piece, Place, MetaPiece
from .. import PieceType, Color
import math

class King(Piece, metaclass=MetaPiece):
    """
    Description:
        King is a Piece in Chess.
        Each player get own King in his/her side.
        The King can move only one step in each direction.
    
    Args:
        Piece (type): King inherits from Piece.
        metaclass (MetaPiece, optional): the meta class is MetaPiece. Defaults to MetaPiece.

    Returns:
        King: King object.
    """
    def __init__(self, color: Color, id):
        super().__init__(PieceType.king, math.inf, (4, 7 * color.value), color, id)
    
    def get_rules(self, positions):
        super().get_rules(positions)
        self.rules.append([pos1 for i in range(self.y - 1, -1, -1) if (pos1 := (self.x, i)) in positions])
        self.rules.append([pos1 for i in range(self.y + 1, 9) if (pos1 := (self.x, i)) in positions])
        self.rules.append([pos1 for i in range(self.x - 1, -1, -1) if (pos1 := (i, self.y)) in positions])
        self.rules.append([pos1 for i in range(self.x + 1, 9) if (pos1 := (i, self.y)) in positions])
        self.rules.append([pos1 for i in range(1, self.x + 1) if (pos1 := (self.x - i, self.y - i)) in positions])
        self.rules.append([pos1 for i in range(1, abs(self.x - 8)) if (pos1 := (self.x + i, self.y + i)) in positions])
        self.rules.append([pos1 for i in range(1, abs(self.x - 8)) if (pos1 := (self.x + i, self.y - i)) in positions])
        self.rules.append([pos1 for i in range(1, self.x + 1) if (pos1 := (self.x - i, self.y + i)) in positions])
        
    
    @Piece.check_pos
    def valid_moves(self, board: list[list[Place]], moves: list[list[tuple]]):
        for i in range(len(moves)):
            if len(moves[i]) == 0:
                continue
            pos = moves[i][0]
            place = board[pos[1]][pos[0]]
            place.protect(self.color)

            if place.is_protected(self.rival):
                moves[i].clear()
                continue
            elif not place.empty:
                if place.piece.color == self.color:
                    moves[i].clear()
                    continue

            if self.first and board[self.pos[1]][self.pos[0]]:
                if self.y == pos[1]:
                    for position in moves[i][:]: 
                        place1 = board[position[1]][position[0]]
                        if (not place1.empty and not (place1.piece.name == PieceType.rook and place1.piece.first)) or place1.is_protected(self.rival):
                            moves[i] = moves[i][:1]
                            break
                    continue
            moves[i] = moves[i][:1]
        return []
