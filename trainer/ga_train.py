import random

from copy import copy, deepcopy
from constants import PlayerAction, GameStatus

MUTATION_RATE = 0.01

def create_random_genes(size):
    ret = []
    for i in range(size):
        ret.append(PlayerAction(random.randrange(0, 3)))
    return ret

def create_population(population_size, step_size):
    ret = []
    for i in range(population_size):
        ret.append(Player(step_size, genes=create_random_genes(step_size)))
    return ret


class Player:
    def __init__(self, step_size, genes, game):
        self.genes = genes
        self.status = GameStatus.ONGOING
        self.step_size = step_size
        self.distance_to_portal = 0
        self.game = game
        self.step = 0

    def clone(self):
        return Player(self.step_size, self.genes)

    def move(self):
        # run out of moves, should die
        if self.step_size < self.step:
            self.status = GameStatus.PLAYER_LOST
        else:
            self.game.move_player(self.genes[self.step])
            self.game.move_enemies()
            self.status = game.status
            self.step += 1

    def update(self):
        if self.status == GameStatus.ONGOING:
            self.move()

    def mutate(self):
        for i in range(len(self.genes)):
            if random() < MUTATION_RATE:
                self.genes[i] = random.randrange(0, 3)

    def calculate_fitness(self):
        fitness = 0
        if self.status == GameStatus.PLAYER_WON:
            fitness = 1.0/16.0 + 10000.0/(self.step * self.step)
        else:
            fitness = 1.0/self.distance_to_portal
        return fitness



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

    def are_all_players_done(self):
        for player in self.population:
            if player.status == GameStatus.ONGOING:
                return False
        return True

    