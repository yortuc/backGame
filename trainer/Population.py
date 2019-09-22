import random
import operator
import math

from Level import Level
from Player import Player
from copy import copy, deepcopy
from constants import PlayerAction, GameStatus, ACTIONS
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
                genes=None,
                mutation_rate=self.mutation_rate
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
        # sort players by fitness
        self.population.sort(key=operator.attrgetter('fitness'), reverse=True)

        top_player = self.population[0]
        self.population = self.population[1:]

        # cross-over
        quarter_count = len(self.population)//4
        best_quarter = self.population[:quarter_count] # first %25
        second_quarter = self.population[quarter_count:quarter_count*2] # second %25
        babies = []
        for i in range(quarter_count):
            p1 = best_quarter[i]
            p2 = second_quarter[i]
            new_genes = []
            for i in range(self.step_size):
                if random.random() < 0.5:
                    new_genes.append(p1.genes[i])
                else:
                    new_genes.append(p2.genes[i])

            baby = Player(step_size=self.step_size, 
                   game=WatchYourBack(Level(deepcopy(self.level_data))), 
                   genes=new_genes,
                   mutation_rate=self.mutation_rate
            )
        babies.append(baby)

        # mutate players
        for player in self.population:
            player.mutate()

        # clone population
        self.population = [top_player] + self.population[:-quarter_count]
        self.population = [
            Player(step_size=self.step_size, 
                   game=WatchYourBack(Level(deepcopy(self.level_data))), 
                   genes=deepcopy(p.genes),
                   mutation_rate=self.mutation_rate
            ) for p in self.population] + babies

    def mutate(self):
        for player in self.population:
            player.mutate()

    def is_all_players_done(self):
        for player in self.population:
            if player.status == GameStatus.ONGOING:
                return False
        return True

    