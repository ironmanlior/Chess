#!/usr/bin/python

from .Base import Piece, MetaPiece, Place
from ..Enum import PieceType, Color

class Bishop(Piece, metaclass = MetaPiece):
    """
    Description:
        Bishop is a Piece in Chess.
        Each player get two Bishops in his/her side.
        The Bishop can move only in diagonal lines.
    
    Args:
        Piece (_type_): Bishop inherits from Piece.
        metaclass (_type_, optional): the meta class is MetaPiece. Defaults to MetaPiece.

    Returns:
        _type_: Bishop object.
    """
    
    def __init__(self, color: Color, id):
        super().__init__(PieceType.bishop, 3, (3 * id + 2, 7 * color.value), color, id)
    
    def get_rules(self, positions):
        super().get_rules(positions)
        self.rules.append([pos1 for i in range(1, self.x + 1) if (pos1 := (self.x - i, self.y - i)) in positions])
        self.rules.append([pos1 for i in range(1, abs(self.x - 8)) if (pos1 := (self.x + i, self.y + i)) in positions])
        self.rules.append([pos1 for i in range(1, abs(self.x - 8)) if (pos1 := (self.x + i, self.y - i)) in positions])
        self.rules.append([pos1 for i in range(1, self.x + 1) if (pos1 := (self.x - i, self.y + i)) in positions])
        
    
    @Piece.check_pos
    def valid_moves(self, board: list[list[Place]], moves):        
        check_moves = []
        threat = []
        for i in range(len(moves)):
            count = 0
            is_king = False
            is_check = False
            first = None
            end = len(moves[i])
            for j in range(len(moves[i])):
                pos = moves[i][j]
                place = board[pos[1]][pos[0]]
                if count == 0: 
                    place.protect(self.color)
                elif count == 1 and is_king:
                    place.protect(self.color)
                    is_king = False
                    break
                if not place.empty:
                    if place.piece.color != self.color:
                        is_king = place.piece.king
                        if count == 0:
                            if is_king:
                                is_check = True
                            end = j + 1
                            first = place.piece
                        if count == 1:
                            if is_king:
                                threat = moves[i][:]
                                threat.append(self.pos)
                                for line in first.rules:
                                    for pos1 in line[:]:
                                        if pos1 not in threat:
                                            line.remove(pos1)
                            break
                        count += 1
                    else:
                        if count == 0:
                            end = j
                        break
            moves[i] = moves[i][:end]
            if is_check:
                check_moves.append(self.pos)
                check_moves.extend(moves[i])
        return check_moves