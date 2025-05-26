#!/usr/bin/python

from __future__ import annotations
from .Pieces.Base import Piece, Place, MetaPiece
from .Enum import PieceType, Color
from .meta_board import MetaBoard
from .Pieces import Pieces, Pawn
from copy import deepcopy

class Board(object, metaclass=MetaBoard):
    def __new__(cls):
        self = super().__new__(cls)
        self.__init__()
        return self        
    
    def __init__(self):
        self.pieces = Pieces()
        self.board = [[Place(x, y) for x in range(8)] for y in range(8)]
        self.selected = None
        self.__place_pieces()
    
    def __eq__(self, other: Board):
        return all([self.board[i][j].piece == other.board[i][j].piece for j in range(8) for i in range(8)])
    
    def __hash__(self):
        return hash(self.board)
    
    def __deepcopy__(self, memo={}):
        new = super().__new__(type(self)) # create new piece of the same type
        memo[id(self)] = self
        new.pieces = deepcopy(self.pieces, memo)
        new.selected = None
        new.board = [[Place(x, y) for x in range(8)] for y in range(8)]
        for color in Color:
            for key in MetaPiece.Pieces:
                for piece in new.pieces[color][key]:
                    new.board[piece.y][piece.x].push(piece)
        return new # return the new piece
    
    def copy(self):
        """return a copy of the board

        Returns:
            Board: copied board
        """
        return deepcopy(self)
    
    def __getitem__(self, y):
        return self.board[int(y) % 8]
    
    def __iter__(self):
        return iter(self.board)
    
    def clear(self):
        """clear protection and available moves
        """
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                self.board[y][x].unprotect()
                if not self.board[y][x].empty:
                    self.board[y][x].piece.clear()
                    self.board[y][x].piece.get_rules(Board.positions)
    
    # select piece from the board
    def select(self, piece: Piece):
        """select piece from the board

        Args:
            piece (Piece): selected piece
        """        
        piece.select()
        self.selected = piece if piece.selected else None

    # move piece on the board
    def move(self, pos: tuple):
        """move piece on the board

        Args:
            pos (tuple): position to move the piece on the board
        """        
        piece = self.selected
        for pawn in self.pieces[piece.color][PieceType.pawn]:
            pawn: Pawn = pawn
            pawn.double_move = False
        try:
            move = self.__castle(piece, pos)
        except Exception:
            try:
                move = self.__en_parsent(piece, pos)
            except Exception:
                move = self.__move(piece.pos, pos) # move piece
        self.select(self.selected) # unselect piece
        return move
    
    def __en_parsent(self, pawn: Pawn, pos: tuple[int, int]):
        assert type(pawn) == Pawn, "mast be pawn"
        pawn.double_move = pawn.first and pos[1] == pawn.pos[1] + 2 * (2 * pawn.rival.value - 1)
        
        move = ""
        if self.board[pos[1]][pos[0]].empty and pos[0] != pawn.pos[0]:
            place = self.board[pawn.pos[1]][pos[0]]
            self.pieces.delete(place.piece)
            place.kill()
            move = "e.p."
        m = self.__move(pawn.pos, pos) # move piece
        move = m if move == "" else move
        if 7 * pawn.rival.value == pawn.y: # if pawn at the end of the board
            pawn.convert(PieceType.queen)
        return move
    
    def __castle(self, piece: Piece, pos: tuple[int, int]):
        y = piece.y
        x1, y1 = pos
        assert piece.king, "mast be king"
        assert piece.first, "mast be the first move"
        assert y == y1, "mast move on x axis"
        move = ""
        if x1 in [6, 7]:
            self.__move((7, y), (5, y)) # move rook
            self.__move(piece.pos, (6, y)) # move king
            move = "O-O-O"
        elif x1 in [2, 1, 0]:
            self.__move((0, y), (3, y)) # move rook
            self.__move(piece.pos, (2, y)) # move king
            move = "O-O"
        return move
    
    def to_mongo(self):
        return [
            [f"{self.board[i][j]}" if self.board[i][j] != None else "" for j in range(8)] for i in range(8)
        ]
    
    @classmethod
    def from_mongo(cls, board) -> Board:
        self = super().__new__(cls)
        self.board = [[Place(x, y) for x in range(8)] for y in range(8)]
        self.pieces.limit = {type: {color: 0 for color in Color} for type in PieceType}
        for i in range(8):
            for j in range(8):
                piece = Piece.from_string(board[i][j])
                self.pieces.Add(piece)
                self.board[i][j].push(piece)
        self.selected = None
        return self

    def __str__(self):
        massage = "\033[H\033[J\n"
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                massage += "     |" if self.board[row][col].empty else f" {self.board[row][col].piece} |"
            massage = massage[:-1] + "\n"
            for col in range(len(self.board[row])):
                massage += "---------"
            massage += massage[:-1] + "\n"
            
        massage = "\n".join(massage.split("\n")[:-2]) + "\n"
        return massage

    def __push_new(self, piecetype: PieceType, color: Color):
        piece = self.pieces.create(piecetype, color)
        self.board[piece.y][piece.x].push(piece)
            
    
    def __place_pieces(self):
        for color in Color:
            for key in MetaPiece.Pieces:
                for _ in range(self.pieces.limit[key][color]):
                    self.__push_new(key, color)
    
    def __move(self, pos: tuple, new_pos: tuple):
        numbers = list(range(1, 9))
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        x, y = pos
        x1, y1 = new_pos
        kill = ""
        piece = self.board[y1][x1].replace(self.board[y][x])
        if piece:
            kill = "x"
            self.pieces.delete(piece)
        return f"{self.board[y1][x1].piece.simbale}{kill}{letters[x1]}{numbers[y1]}"


        