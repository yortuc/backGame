import random
from constants import PlayerAction, GameStatus

ACTIONS = [PlayerAction.UP, PlayerAction.RIGHT, PlayerAction.DOWN, PlayerAction.LEFT]

class Player:
    def __init__(self, step_size, game, genes):
        self.genes = self.create_random_genes(step_size) if genes is None else genes
        self.status = GameStatus.ONGOING
        self.step_size = step_size
        self.distance_to_portal = 0
        self.game = game
        self.step = 0
        self.fitness = 0
        self.mutation_rate = 0.01

    def create_random_genes(self, size):
        ret = []
        for i in range(size):
            ret.append(ACTIONS[random.randrange(0, 3)])
        return ret

    def clone(self):
        return Player(self.step_size, self.game, self.genes)

    def move(self):
        # run out of moves, should die
        if self.step_size < self.step:
            self.status = GameStatus.PLAYER_LOST
        else:
            self.game.move_player(self.genes[self.step])
            if self.game.status == GameStatus.ONGOING:
                self.game.move_enemies()
            self.status = self.game.status
            self.step += 1

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
            fitness = 1.0/self.distance_to_portal
        self.fitness = fitness
