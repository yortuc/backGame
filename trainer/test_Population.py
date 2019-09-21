from Level import Level
from Player import Player
from Population import Population

def test_init_population():
    population = Population(
        population_size=10,
        step_size=5, 
        level=Level([
            [0, 0, 2],
            [0, 0, 0],
            [3, 0, 0]
        ])
    )
    for i in range(10):
        assert isinstance(population.population[i], Player) == True

def test_calculate_fitness():
    population = Population(
        population_size=10, 
        step_size=5,
        level=Level([
            [0, 0, 2],
            [0, 0, 0],
            [3, 0, 0]
        ])
    )
    population.update()
    population.calculate_fitness()

    for player in population.population:
        assert player.fitness != 0

def test_player_dies_when_step_size_reached():
    population = Population(
        population_size=1,
        step_size=1,
        level=Level([
            [0, 2, 0],
            [0, 0, 0],
            [3, 0, 0]
        ])
    )
    population.update()
    population.update()
    assert population.is_all_players_done() == True

def test_natural_selection():
    population = Population(
        population_size=10, 
        step_size=2,
        level=Level([
            [0, 0, 2],
            [0, 0, 0],
            [3, 0, 0]
        ])
    )
    
    while not population.is_all_players_done():
        population.update()
        population.calculate_fitness()
        population.natural_selection()

    assert True == True
