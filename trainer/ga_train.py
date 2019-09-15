import random
from constants import PlayerAction

def create_random_genes(size):
    ret = []
    for i in range(size):
        ret.append(PlayerAction(random.randrange(0, 3)))

class Player:
    def __init__(self, step_size):
        self.genes = create_random_genes(step_size)