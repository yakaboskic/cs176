from MapColoringProblem import MapColoringProblem, MapColoringSolution
from SAT import SAT
import random


if __name__ == '__main__':
    random.seed(1)
    
    #-- Run with GSAT
    map_problem = MapColoringProblem('mapColoring.cnf')
    solution = MapColoringSolution(map_problem)
    solver = SAT(map_problem, solution)
    solution = solver.gsat()
    print(solution)

    #-- Run with WalkSAT
    solution = MapColoringSolution(map_problem)
    solver = SAT(map_problem, solution)
    solution = solver.walk_sat()
    print(solution)
