from map_utilities import clear_console_output
from Level import Level
from Population import Population

level_data = [
    [6, 0, 0, 3],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 2]
]

level_data2 = [
    [6,0,0,0,3,0,0,6],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,0,0,1,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0]
]

level_data3 = [
    [1,1,0,2,0,0,1,1],
    [0,0,0,0,0,0,1,1],
    [0,1,1,0,1,0,1,1],
    [0,1,1,0,1,0,0,1],
    [0,1,1,0,0,0,0,1],
    [0,1,1,0,0,0,0,1],
    [6,6,0,0,0,0,0,1],
    [3,0,0,0,0,0,1,1]
]

population = Population(
    population_size=100,
    step_size=25,
    level_data=level_data3,
    mutation_rate=0.1
)

for generation in range(50000):
    # play them until every player is done
    while not population.is_all_players_done():
        population.update()

    population.calculate_fitness()
    
    clear_console_output()
    print(f"Generation: #{generation}")
    print("Genes \t Fitness")
    for player in population.population[:5]:
        print(f"{[k.value for k in player.genes[:player.step]]} \t {player.fitness} \t {player.status}")
    print("---------")

    # evolve population
    population.natural_selection()