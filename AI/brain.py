from __future__ import annotations
from Engine import Game, Board, Piece, Color, PieceType
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, InputLayer, Flatten
import tensorflow as tf
import numpy as np
import telepot
import random
import math
import io

TOKEN = "1082000037:AAHfoPgVqYTIxeALJnPNqtBvLBTR3OCX_tI"
bot = telepot.Bot(TOKEN)

bin_board = [[PieceType.null for _ in range(8)] for _ in range(8)]

def send_message(massage):
    try:
        chat_id = 1203979488
        bot.sendMessage(chat_id, massage)
    except Exception as e:
        print(e)

class Model(object):
    count = {Color.black: 0, Color.white: 0}
    def __init__(self, color: Color):
        self.color = color
        self.id = Model.count[color]
        Model.count[color] += 1
        
        self.neural_input = None
        self.model = Sequential()
        self.model.add(Dense(10, input_shape=(256,)))
        self.model.add(Dense(10, activation="relu"))
        self.model.add(Dense(80, activation="relu"))
        self.model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])

        

    def predict(self, game: Game):
        prediction = self.model.predict(self.neural_input)[0]
        pieces = game.board.pieces[self.color]
        count = 0
        for name in pieces:
            for piece in pieces[name]:
                count += 1
                if piece.killed:
                    prediction[count] = 0
        prediction = [[pieces[i], prediction[i]] for i in range(16)]
        piece = max(prediction, key=lambda x: x[1])[0]
        piece = game.board.pieces[self.color][piece[0]][piece[1]]
        return piece
    
    def predict_pos(self, piece: Piece, game: Game):
        best_prediction = -math.inf
        best_position = (-1, -1)
        for move in piece.moves:
            game.move(piece, move)
            prediction_dict = {}
            prediction = self.model.predict(self.neural_input)[0]
            prediction_dict[Color.white] = prediction[0]
            prediction_dict[Color.black] = prediction[1]
            game.undo()
            if prediction_dict[self.color] >= best_prediction:
                if prediction_dict[self.color] >= prediction_dict[self.rival]:
                    if prediction_dict[self.color] >= .9:
                        return move
                    else:
                        best_prediction = prediction_dict[self.color]
                        best_position = move
        return best_position
    
    def predict(self, game: Game):
        self.neural_input = np.array([game.board.bin_board])
        piece = self.predict_piece(game.board)
        move = self.predict_pos(piece, game)
        return (piece, move)

    def save(self, id_num: int):
        self.model.save(f"models/{self.color}/model{id_num}1.h5")
        
    def load(self, id_num: int):
        self.model = keras.models.load_model(f"models/{self.color}/model{id_num}1.h5")
        
    def get_weights(self):
        return self.model.get_weights()
        
    def set_weights(self, weights: list[list]):
        return self.model.set_weights(weights)
    
    def mutate(self):
        for index in range(2):
            weights = self.get_weights(index)
            for i in range(len(weights)):
                for j in range(len(weights[i])):
                    if random.uniform(0,1) < .85:
                        weights[i][j] += random.uniform(-.5, .5)
            self.set_weights(index, weights)
    
    def model_crossover(self: Model, other: Model):
        output = [[], []]
        for index in range(2):
            weight1 = self.get_weights(index)
            weight2 = other.get_weights(index)

            for i in range(len(weight1)):
                for j in range(len(weight1[i])):
                    if random.uniform(0, 1) > .5:
                        weight1[i][j], weight2[i][j] = weight2[i][j], weight1[i][j]
            output[0].append(weight1)
            output[1].append(weight2)

        return np.array(output)
    
    def __str__(self):
        stream = io.StringIO()
        self.model.summary(print_fn=lambda x: stream.write(x + '\n'))
        summary = stream.getvalue()
        stream.close()
        
        massage = ""
        massage += f"color: {self.color}\n\n"
        massage += f"id: {self.id}\n\n"
        for val in self.score:
            massage += f"number of {val}s: {self.score[val]}\n"
        massage += "\n"
        massage += f"fitness: {self.fitness}\n\n"
        massage += f"{summary}\n\n"
        send_message(massage)
        return massage
            


