Level solver with genetic algorithm:
- genes are directions to go
- fixed size of steps (100) [up, left, right, left, left ...]
- dies if gets eaten by spiders or when run out of directions (means got stuck)
- fitness value is died how far from the portal or if reached the portal,
how many steps it took to reach.