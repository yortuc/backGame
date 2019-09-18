import random
import operator

from Player import Player
from copy import copy, deepcopy
from constants import PlayerAction, GameStatus
from WYB import WatchYourBack

class Population:
    def __init__(self, population_size, level):
        self.level = level
        self.size = population_size
        self.mutation_rate = 0.01
        self.population = self.create_population()

    def create_population(self):
        ret = []
        for i in range(self.size):
            new_player = Player(
                step_size=100, 
                game=WatchYourBack(self.level),
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
        self.population.sort(key=operator.attrgetter('fitness'))

        # take top half
        half_size = int(len(self.population)/2)
        best_players = self.population[:half_size]

        # mutate the rest
        worse_players = self.population[half_size:]
        for p in worse_players:
            p.mutate()

        # create next generation
        self.population = best_players + worse_players

    def mutate(self):
        for player in self.population:
            player.mutate()

    def is_all_players_done(self):
        for player in self.population:
            if player.status == GameStatus.ONGOING:
                return False
        return True

    