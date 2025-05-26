#!/usr/bin/python

from .board import Board
from .clock import ChessClock
from .Enum import Color, Status, PieceType
from DataStructure import Stack
from .Pieces.Base import Place

from datetime import timedelta

class Game(object):
    def __init__(self, game_time: timedelta = None):
        self.board = Board()
        self.current = [color for color in Color]
        self.status: Status = Status.null
        self.clock = ChessClock(game_time) if game_time and game_time.total_seconds() else None
        self.moves: list[str] = []
        self.past = Stack()
        self.future = Stack()
        self.past.push(self.board)
        self.board = self.board.copy()
        self.pieces = self.board.pieces
        self.selected = False
        self.view_mode = False
        self.valid_moves = []
        self.Status()
        if game_time == 0: self.k = 0
        elif 300 <= game_time <= 3600: self.k = 10
    
    def Status(self):
        """update the status of the game and generate valid moves
        """
        self.check_timer()
        self.valid_moves = 0
        self.status = Status.null
        allowed_moves = self.__update_moves()
        king = self.pieces[self.current[0]][PieceType.king][0]
        self.status = Status.check if self.board[king.y][king.x].is_protected(self.current[1]) else Status.null
            
        for piece_name in self.pieces[self.current[0]]:
            for piece in self.pieces[self.current[0]][piece_name]:
                if self.status == Status.check:
                    if not piece.killed and not piece.king:
                        def func(move):
                            return not len(allowed_moves) or len([None for moves in allowed_moves if move in moves])
                        piece.moves = list(filter(func, piece.moves))
                if not piece.killed:
                    self.valid_moves += len(piece.moves)
        
        if not self.valid_moves:
            self.status = Status.mate if self.status == Status.check else Status.pate
            self.moves[-1] += "#" if self.status == Status.mate else ""
        if self.status == Status.check:
            self.moves[-1] += "+" if self.status == Status.mate else ""
        return None
    
    def unselect(self):
        assert self.is_selected() and self.board.selected, "must be a selected piece"
        assert self.board.selected.selected
        self.selected = False
        self.board.selected.select()
        self.board.selected = None
    
    def check_timer(self):
        try:
            if self.clock: self.clock.update()
        except TimeoutError as e:
            self.status = Status.time_up
            raise e
    
    def select(self, place: Place):
        """select place from the board

        Args:
            place (Place): the place to select
        """
        assert not place.empty, "this place is empty"
        assert place.piece.color == self.current[0], "wait for your turn"
        assert not self.is_selected(), "you already selected a place"
        self.board.select(place.piece)
        self.selected = True
    
    def is_selected(self) -> bool:
        """return true if some piece is selected else return false
        
        Returns:
            bool: is some piece is selected
        """
        return self.selected
    
    def move(self, pos: tuple) -> None:
        """move the selected piece on the board

        Args:
            pos (tuple): position to move to
        """
        try:
            assert self.board.selected, "selected can't be None"
            assert self.future.isEmpty(), "you are in view mode"
            assert pos in self.board.selected.moves, "this position is not available for the selected piece"
        except Exception as e:
            self.unselect()
            raise
        self.moves.append(self.board.move(pos))
        self.past.push(self.board)
        self.board = self.board.copy()
        self.pieces = self.board.pieces
        self.current.reverse()
        if self.clock: self.clock.swich()
        self.board.selected = None
        self.selected = False
    
    def undo(self):
        """return to last move
        """
        self.selected = False
        assert self.future.isEmpty(), "you are in view mode, please move forward"
        assert not self.past.isEmpty(), "there is no past"
        
        self.board: Board = self.past.pop().copy()
        self.pieces = self.board.pieces
        self.current.reverse()
        self.Status()
    
    def enter_view_mode(self):
        assert not self.view_mode
        self.view_mode = True
        self.board: Board = self.past.pop()
        self.pieces = self.board.pieces
        
    def exit_view_mode(self):
        assert self.view_mode
        self.view_mode = False
        self.past.push(self.board)
        self.board = self.board.copy()
        self.pieces = self.board.pieces
        self.Status()
    
    def backward(self):
        assert not self.past.isEmpty(), "can't move backward"
        if not self.view_mode:
            self.enter_view_mode()
        self.future.push(self.board)
        self.board: Board = self.past.pop()
        self.pieces = self.board.pieces
    
    def forward(self):
        if  not self.future.isEmpty():
            if not self.view_mode:
                self.enter_view_mode()
            self.past.push(self.board)
            self.board: Board = self.future.pop()
            self.pieces = self.board.pieces
            try:
                assert not self.future.isEmpty(), "can't move forward"
            except Exception as e:
                self.exit_view_mode()
                raise
    
    def __update_moves(self) -> list:
        self.board.clear()
        allowed_moves = []
        for color in Color:
            for piece_name in self.pieces[color]:
                for piece in self.pieces[color][piece_name]:
                    if not piece.king:
                        allowed = piece.valid_moves(self.board)
                        if not piece.killed and len(allowed) > 0:
                            allowed_moves.append(allowed)
        for color in Color:
            self.pieces[color][PieceType.king][0].valid_moves(self.board)
        return allowed_moves
