import random
import operator

from Level import Level
from Player import Player
from copy import copy, deepcopy
from constants import PlayerAction, GameStatus
from WYB import WatchYourBack

class Population:
    def __init__(self, population_size, step_size, level_data, mutation_rate=0.01):
        self.level_data = level_data
        self.population_size = population_size
        self.step_size = step_size
        self.mutation_rate = mutation_rate
        self.population = self.create_population()

    def create_population(self):
        ret = []
        for i in range(self.population_size):
            new_player = Player(
                step_size=self.step_size, 
                game=WatchYourBack(Level(deepcopy(self.level_data))),
                genes=None
            )
            ret.append(new_player)
        return ret

    def calculate_fitness(self):
        for player in self.population:
            player.calculate_fitness()

    def update(self):
        for player in self.population:
            player.update()
        
    def natural_selection(self):
        # sor players by fitness
        self.population.sort(key=operator.attrgetter('fitness'), reverse=True)

        top_player = self.population[0]
        self.population = self.population[1:]

        for player in self.population:
            player.mutate()

        self.population = [top_player] + self.population

    def mutate(self):
        for player in self.population:
            player.mutate()

    def is_all_players_done(self):
        for player in self.population:
            if player.status == GameStatus.ONGOING:
                return False
        return True

    