Level solver with genetic algorithm:
- genes are directions to go
- fixed size of steps (100) [up, left, right, left, left ...]
- dies if gets eaten by spiders or when run out of directions (means it got stuck)
- fitness value depends on how far player died from the portal or if reached the portal, how many steps it took to reach. (less is better)



Population
    - create random population
        - create players with random genes
    
    - run the generation
        - play with each player
        - when everybody dies, calculate fitness values
        - order by fitness values 
        - do natural selection: create next generation of players
    
    - run the generation

    - after enough generations, take the best player as solution.



