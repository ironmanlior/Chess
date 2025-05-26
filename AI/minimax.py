from Engine import Game, Board, Color, Status
from Engine.Pieces import Piece

class MiniMax(object):
    def __init__(self, level: int = 10):
        self.level = level
        self.history: dict[Board, float] = {}
    
    @property
    def level(self):
        return self.__level
    
    @level.setter
    def level(self, value):
        assert value >= 1 and value <= 30, "level must be between 1 and 30"
        self.__level = value
    
    def evaluate_move(self, game: Game, piece: Piece, move: tuple) -> float:
        killed = game.board[move[1]][move[0]].piece
        score = killed.value if killed else 0
        game.select(game.board[piece.y][piece.x])
        game.move(move)
        game.Status()
        return score
    
    def evaluate(self, game: Game, color: Color, count: int) -> float:
        if count > 0:
            m = 2 * abs(color.value - game.current[1].value) - 1
            for piece_name in game.pieces[game.current[0]]:
                for piece in game.pieces[game.current[0]][piece_name]:
                    for move in piece.moves:
                        try:
                            score = self.history[(game.board, game.current[0])]
                        except KeyError:
                            score = m * self.evaluate_move(game, piece, move)
                            score += self.evaluate(game, count - 1) if game.status in [Status.null, Status.check] else 20 * m * count
                            self.history[(game.board, game.current[0])] = score
                            game.undo()
        return score
    
    def predict(self, game: Game) -> tuple:
        moves = []
        for piece_name in game.board.pieces[game.current[0]]:
            for piece in game.board.pieces[game.current[0]][piece_name]:
                for move in piece.moves:
                    self.history: dict[Board, float] = {}
                    score = self.evaluate_move(game, piece, move)
                    score += self.evaluate(game, game.current[0], self.level) if game.status in [Status.null, Status.check] else (self.level + 1) * 20
                    game.undo()
                    moves.append({"piece": piece, "move": move, "score": score})
        return max(moves, key=lambda move: move["score"])