import math
import random

from constants import PlayerAction, GameStatus, ACTIONS

class Player:
    def __init__(self, step_size, game, genes, mutation_rate=0.01):
        self.genes = self.create_random_genes(step_size) if genes is None else genes
        self.status = GameStatus.ONGOING
        self.step_size = step_size
        self.game = game
        self.step = 0
        self.fitness = 0
        self.mutation_rate = mutation_rate
        self.last_pos = self.game.level.get_player_pos()
        self.win_steps = -1

    def create_random_genes(self, size):
        ret = []
        for i in range(size):
            ret.append(ACTIONS[random.randrange(0, 3)])
        return ret

    def clone(self):
        return Player(self.step_size, self.game, self.genes)

    def move(self):
        self.last_pos = self.game.level.get_player_pos()
        if self.step < self.step_size:
            if self.game.move_player(self.genes[self.step]) == False:
                self.status = GameStatus.PLAYER_LOST
                return

            if self.game.status == GameStatus.ONGOING:
                self.game.move_enemies()
            self.status = self.game.status
            self.step += 1
        else:
            self.status = GameStatus.PLAYER_LOST

    def update(self):
        if self.status == GameStatus.ONGOING:
            self.move()

    def mutate(self):
        for i in range(len(self.genes)):
            if random.random() < self.mutation_rate:
                self.genes[i] = ACTIONS[random.randrange(0, 3)]

    def calculate_fitness(self):
        fitness = 0
        if self.status == GameStatus.PLAYER_WON:
            fitness = 10000.0/(self.step * self.step)
        else:
            player_pos = self.last_pos
            portal_pos = self.game.level.get_portal_pos()
            distance_to_portal = math.sqrt((player_pos[1] - portal_pos[1])**2 + (player_pos[0] - portal_pos[0])**2)
            fitness = 1.0/distance_to_portal
        self.fitness = fitness
