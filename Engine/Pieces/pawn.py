#!/usr/bin/python

from ..Enum import PieceType, Color
from .Base import MetaPiece, Piece, Place

class Pawn(Piece, metaclass=MetaPiece):    
    """
    Description:
        Pawn is a Piece in Chess.
        Each player get 8 Pawns in his/her side.
        The Pawn can move own/two steps forward in the first move.
        The Pawn can move own steps forward pieces.
    
    Args:
        Piece (type): Pawn inherits from Piece
        metaclass (MetaPiece, optional): the meta class is MetaPiece. Defaults to MetaPiece.

    Returns:
        Pawn: Pawn object
    """
    def __init__(self, color: Color, id):
        super().__init__(PieceType.pawn, 1, (id, 5 * color.value + 1), color, id)
        self.double_move = False

    def convert(self, Type: PieceType) -> None:
        self.__class__ = MetaPiece.Pieces[Type]
        piece: Piece = MetaPiece.Pieces[Type](self.color, self.id)
        piece.move(self.pos)
        piece.selected = self.selected
        self.__dict__.update(vars(piece))
    
    def get_rules(self, positions):
        super().get_rules(positions)
        c = (2 - 2 * self.color.value) - 1
        self.rules.extend([[pos1] if (pos1 := (self.pos[0] + i, self.pos[1] + c)) in positions else [] for i in [-1, 1]])
        self.rules.append([pos1 for i in [1, 2] if (self.first or i != 2) and (pos1 := (self.pos[0], self.pos[1] + i * c)) in positions])
    
    @Piece.check_pos
    def valid_moves(self, board: list[list[Place]], moves: list[list[tuple]]):
        check_moves = []
        
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                pos = moves[i][j]
                place = board[pos[1]][pos[0]]
                if i < 2:
                    place.protect(self.color)
                    if not place.empty:
                        if place.piece.color == self.color:
                            moves[i].clear()
                        else:
                            if place.piece.king:
                                check_moves.append(self.pos)
                    else:
                        place1 = board[self.pos[1]][pos[0]]
                        if not place1.empty:
                            if place1.piece.pawn:
                                if place1.piece.double_move:
                                    
                                    break
                        moves[i].clear()
                    break
                else:
                    if not place.empty:
                        moves[i] = moves[i][:j]
                        break
        return check_moves
    
#  or not self.first