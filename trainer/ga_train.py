from Level import Level
from Population import Population

level_data = [
    [6, 0, 0, 3],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 2]
]

population = Population(
    population_size=10,
    step_size=5,
    level_data=level_data
)

for generation in range(1000):
    # play them until every player is done
    while not population.is_all_players_done():
        population.update()

    population.calculate_fitness()
    print(f"Generation: #{generation}")
    print("Genes \t Fitness")
    for player in population.population:
        print(f"{[k.value for k in player.genes[:player.step]]} \t {player.fitness}")
    print("---------")

    # evolve population
    population.natural_selection()