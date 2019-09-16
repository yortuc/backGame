import random

from Player import Player
from copy import copy, deepcopy
from constants import PlayerAction, GameStatus

def create_population(population_size, step_size):
    ret = []
    for i in range(population_size):
        ret.append(Player(step_size, genes=create_random_genes(step_size)))
    return ret


class Population:
    def __init__(self, size):
        self.population = create_population(size, step_size=100)

    def calculate_fitness(self):
        for player in self.population:
            player.calculate_fitness()

    def update(self):
        for player in self.population:
            player.update()
        
    def natural_selection(self):
        pass

    def mutate(self):
        pass

    def is_all_players_done(self):
        for player in self.population:
            if player.status == GameStatus.ONGOING:
                return False
        return True

    