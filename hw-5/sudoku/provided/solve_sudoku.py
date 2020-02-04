from display import display_sudoku_solution
import random, sys
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:

    random.seed(3)

    #-- Set up Problem
    problem = SudokuProblem('rules.sud', cnf_filename='rules.cnf')

    #-- Set up Solver
    sat = SAT(problem, threshold=.35, iteration_limit=10000)

    #-- Run WalkSAT or GSAT
    solution = sat.walk_sat_2()

    #-- Print Solution
    print(solution)
