from __future__ import annotations
from copy import deepcopy
from ...Enum import Color, PieceType

positions = [(j, i) for j in range(8) for i in range(8)]

class Piece(object):
    """Piece base class

    Args:
        object (type): Piece inherits from object

    Returns:
        Piece: Piece object
    """
    
    types = {}
    def __init__(self, name: PieceType, value: float, pos: tuple[int, int], color: Color, id: int):
        """initialize Piece object

        Args:
            name (PieceType): name of the piece
            value (float): value of the piece
            pos (tuple[int, int]): position of the piece
            color (Color): color of the piece
            id (int): piece id
        """        
        self.name = name # piece name
        self.color = color # piece color
        self.rival = Color(1 - color.value) # piece rival
        self.value = value # piece value
        self.id = id # piece id
        self.x, self.y = self.pos = pos # piece pos (x, y)
        self.simbale = ""
        if name == PieceType.rook:
            self.simbale = "R"
        elif name == PieceType.knight:
            self.simbale = "N"
        elif name == PieceType.bishop:
            self.simbale = "B"
        elif name == PieceType.queen:
            self.simbale = "Q"
        elif name == PieceType.king:
            self.simbale = "K"
        self.img = f"App/Media/Pieces/{self.color.name[0].upper()}{self.color.name[1:]}/{self.name.name}.png" # piece image
        self.bin = [color.value] # piece binary presentation
        self.bin.extend(name.value)
        self.king = name == PieceType.king # is piece king
        self.pawn = name == PieceType.pawn # is piece pawn
        self.killed = False # is piece killed
        self.first = True # is piece haven't moved
        self.selected = False # is piece selected
        self.moves: list[tuple] = [] # available moves list of the piece
        self.rules = self.get_rules(positions)

    def __hash__(self):
        return hash((self.name, self.color, self.id, self.pos))
    
    def get_rules(self, positions):
        """get the piece moving rules

        Args:
            positions (_type_): list of positions on the board

        Returns:
            _type_: list of positions on the board that allowed by the piece rules
        """        
        self.rules = []
        return []
    
    def __eq__(self, other: Piece):
        return self.color == other.color and self.name == other.name and self.pos == other.pos
    
    def __deepcopy__(self, memo={}):
        """copy the piece

        Args:
            memo (dict, optional): dictionary of object id to object. Defaults to {}.

        Returns:
            _type_: copy of the piece
        """        
        if self.pawn:
            memo = memo
        new = super().__new__(type(self)) # create new piece of the same type
        memo[id(self)] = self
        for k, v in vars(self).items(): # loop through the piece attributes
            setattr(new, k, deepcopy(v, memo)) # create deep copy of the attribute
        return new # return the copied piece
    
    @staticmethod
    def check_pos(func):
        """eliminate the positions that the that can't be happening

        Args:
            func (_type_): function to wrap
        """        
        def wrapper(self: Piece, board):
                moves = self.rules.copy()
                check_moves = func.__get__(self)(board, moves)
                for line in moves:
                    self.moves.extend(line)
                return check_moves
        return wrapper

    def valid_moves(self, board, moves):
        """eliminate the positions that the that can't be happening

        Args:
            board (_type_): current board placement
            moves (_type_): moves allowed by the piece rules

        Returns:
            _type_: moves allowed by the game rules
        """        
        return []
    
    def select(self):
        """select or deselect the piece
        """        
        self.selected = not self.selected
    
    def clear(self):
        """clear piece moves
        """        
        self.moves.clear()
    
    def move(self, new_pos):
        """moves piece and then clear moves

        Args:
            new_pos (_type_): the piece new position
        """        
        self.pos = self.x, self.y = new_pos
        self.clear()
    
    def kill(self):
        """killing the piece
        """        
        self.killed = True
    
    @classmethod
    def from_string(cls, string) -> Piece:
        """get string and return Piece object

        Args:
            string (_type_): _description_

        Returns:
            Piece: _description_
        """        
        types = {
            "♜": [PieceType.rook, Color.white],
            "♖": [PieceType.rook, Color.black],
            "♞": [PieceType.knight, Color.white],
            "♘": [PieceType.knight, Color.black],
            "♝": [PieceType.bishop, Color.white],
            "♗": [PieceType.bishop, Color.black],
            "♛": [PieceType.queen, Color.white],
            "♕": [PieceType.queen, Color.black],
            "♚": [PieceType.king, Color.white],
            "♔": [PieceType.king, Color.black],
            "♟": [PieceType.pawn, Color.white],
            "♙": [PieceType.pawn, Color.black]
        }
        cls = Piece.types[types[string[0]][0]]
        return cls(types[string[0]][1], int(string[1]))
        
    def __str__(self):
        pieces = {
            PieceType.rook: {Color.white: "♜", Color.black: "♖"},
            PieceType.knight: {Color.white: "♞", Color.black: "♘"},
            PieceType.bishop: {Color.white: "♝", Color.black: "♗"},
            PieceType.queen: {Color.white: "♛", Color.black: "♕"},
            PieceType.king: {Color.white: "♚", Color.black: "♔"},
            PieceType.pawn: {Color.white: "♟", Color.black: "♙"},
        }
        return f"{pieces[self.name][self.color]}{self.id}"