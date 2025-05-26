#!/usr/bin/python

from __future__ import annotations
import mongoengine as db
from Engine import Game, Board, Color, Status
from .user import User

class GameDB(db.Document):
    time_line = db.ListField(db.ListField(db.ListField(db.StringField())), required=True)
    players = db.ListField(db.ReferenceField(User))
    status = db.EnumField(Status)
    
    def __init__(self, game: Game, players: list[User], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_line = []
        game.past.push(game.board)
        while not game.future.isEmpty():
            game.past.push(game.future.pop())
        while not game.past.isEmpty():
            board: Board = game.past.pop()
            self.time_line.insert(0, board.to_mongo())
        self.players = players
        self.status = game.status
    
    @db.queryset_manager
    def objects(cls, query: db.QuerySet) -> db.QuerySet:
        return query
    
    def from_mongo(self) -> tuple[Game, list[User]]:
        game = Game()
        game.current = [color for color in Color]
        if len(self.time_line) % 2 == 0:
            game.current.reverse()
        game.status = self.status
        for board_mongo in self.time_line:
            game.past.push(Board.from_mongo(board_mongo))
        board: Board = game.past.pop()
        game.board = board
        game.pieces = game.board.pieces
        return game, self.players
    
