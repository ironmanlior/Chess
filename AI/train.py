from Engine import Piece, Color, Game, Board
from brain import Model, send_message, model_crossover
from minimax import MiniMax
import math, random

class Train(object):
    def __init__(self, color: Color=Color.white, total_models: int=30, generation_num: int=100, debug: bool=False):
        self.generation_num = generation_num
        self.generation = 0
        self.simulation_num = 0
        self.last_best_fitness_models: list[Model] = []
        self.last_best_fitness = [-math.inf, -math.inf]
        self.best_fitness_models = list()
        self.length = total_models
        self.flags = debug
        self.color: Color = color
        self.rival: Color = Color(1 - self.color.value)
        self.population = [Model(color) for _ in range(total_models)]
        self.minimax = MiniMax(self.rival)
        for model in self.population: model.mutate()
    
    def send_generation(self) -> None:
        if self.flags:
            send_message(f"{self.generation = }")

    def print_range(self, num, total) -> str:
        present = (100 * num) / total
        massage = f"total: {total} -> {present}%\n"
        massage += "["
        for _ in range(int((present / 10) * 10)):
            massage += "#"
        for _ in range(100 - int((present / 10) * 10)):
            massage += " "
        massage += "]\n\n"
        return massage
    
    def debug(self) -> str:
        if self.flags:
            print("\033[H\033[J")
            total_num = self.generation_num * self.length
            total = (self.generation * self.length) + self.simulation_num
            massage = ""
            massage += self.print_range(total, total_num)
            massage += self.print_range(self.generation, self.generation_num)
            massage += self.print_range(self.simulation_num, self.length)
            return massage
    
    def simulation(self) -> str:
        game = Game(is_gui=False)
        players: dict[Color, Player] = {
            self.color: self.population[self.simulation_num],
            self.rival: self.minimax
        }
        print(game.board, end="\n\n\n")
        while True:
            for color in Color:
                player = players[color]
                move = player.predict(game)
                player.fitness += player.evaluate_move(game, move[0], move[1])
                print(game.board, end="\n\n\n")
                if game.board.is_mate:
                    player.score[color] += 1
                    return None
    
    def calc_fitness(self):
        if self.flags:
            self.send_generation()
        for self.simulation_num in range(len(self.population)):
            if self.flags:
                self.debug()
            self.population[self.simulation_num] = self.simulation()

    def best_two_parents(self):
        self.population.sort(key=lambda player: player.fitness, reverse=True)
        self.best_fitness_models = self.population[2:]
        
    def create_next_generation(self):
        def new_model():
            model = Model(self.color) # create a Model object
            weights = model_crossover(self.last_best_fitness_models[0], self.last_best_fitness_models[1]) # crossover the two winners models
            model.set_weights(random.choice(weights)) # set the crossover weights
            model.mutate() # mutate model
            return model
        self.population = [new_model() for _ in range(self.length)]

    def run(self):
        def update(num: int):
            updated = self.best_fitness_models[num] >= self.last_best_fitness_models[num]
            if updated:
                self.last_best_fitness_models[num] = self.best_fitness_models[num]
                self.best_fitness_models[num].save(num)
                if self.flags:
                    print(self.best_fitness_models[num], end="\n\n\n")
        for self.generation in range(self.generation_num):
            self.calc_fitness() # calculate the fitness of all the population
            self.best_two_parents()
            update(0)
            update(1)
            self.create_next_generation()

if __name__ == "__main__":
    color = Color["black"]
    train = Train(color=color, debug=True)
    train.run()