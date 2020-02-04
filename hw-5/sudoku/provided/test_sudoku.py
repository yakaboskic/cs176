from SudokuProblem import SudokuProblem, SudokuSolution
from SAT import SAT
import random
import time

def test1():
    print('Test 1: Sudoku with GSAT for one_cell.cnf')
    random.seed(1)
    problem = SudokuProblem('one_cell.sud', cnf_filename='one_cell.cnf')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, iteration_limit=10000)
    solution = sat.gsat()
    print(solution)
    print('\n')

def test2():
    print('Test 2: Sudoku with GSAT for all_cells.cnf')
    random.seed(1)
    problem = SudokuProblem('all_cells.sud', cnf_filename='all_cells.cnf')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, iteration_limit=10000)
    solution = sat.gsat()
    print(solution)
    print('\n')


# Solves one_cell.cnf. Iterations= 4 
def test11():
    print('Test 11: Sudoku with WalkSAT for one_cell.cnf')
    random.seed(3)
    problem = SudokuProblem('one_cell.sud', cnf_filename='one_cell.cnf')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, threshold=.35, iteration_limit=10000)
    solution = sat.walk_sat()
    print(solution)
    print('\n')

# Solves all_cells.cnf. Iterations= 314
def test12():
    print('Test 12: Sudoku with WalkSAT for rules.cnf')
    random.seed(3)
    problem = SudokuProblem('all_cells.sud', cnf_filename='all_cells.cnf')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, threshold=.35, iteration_limit=10000)
    solution = sat.walk_sat()
    print(solution)
    print('\n')

# Solves rows.cnf. Iterations= 488
def test13():
    print('Test 13: Sudoku with WalkSAT for rows.cnf')
    random.seed(3)
    problem = SudokuProblem('rows.sud', cnf_filename='rows.cnf')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, threshold=.35, iteration_limit=10000)
    solution = sat.walk_sat()
    print(solution)
    print('\n')

# Solves rows_and_cols.cnf. Iterations= 1744
def test14():
    print('Test 14: Sudoku with WalkSAT for rows_and_cols.cnf')
    random.seed(3)
    problem = SudokuProblem('rows_and_cols.sud', cnf_filename='rows_and_cols.cnf')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, threshold=.35, iteration_limit=10000)
    solution = sat.walk_sat()
    print(solution)
    print('\n')

# Solves rules.cnf. Iterations= 4710 
def test3():
    print('Test 3: Sudoku with WalkSAT for rules.cnf')
    random.seed(3)
    problem = SudokuProblem('rules.sud', cnf_filename='rules.cnf')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, threshold=.35, iteration_limit=10000)
    solution = sat.walk_sat()
    print(solution)
    print('\n')

# Solves puzzle1.sud. Iterations = 18,270.
def test4():
    print('Test 4: Sudoku with WalkSAT for Puzzle 1')
    random.seed(3)
    problem = SudokuProblem('puzzle1.sud')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, threshold=.35, iteration_limit=100000)
    solution = sat.walk_sat()
    print(solution)
    print('\n')

# Solves puzzle2.sud. Iterations = 34,962.
def test5():
    print('Test 5: Sudoku with WalkSAT for Puzzle 2')
    random.seed(3)
    problem = SudokuProblem('puzzle2.sud')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, threshold=.35, iteration_limit=100000)
    solution = sat.walk_sat()
    print(solution)
    print('\n')


# Solves puzzle_bonus.sud. Iterations = 71,095.
def test6():
    print('Test 6: Sudoku with WalkSAT for Puzzle Bonus')
    random.seed(4)
    problem = SudokuProblem('puzzle_bonus.sud')
    solution = SudokuSolution(problem) 
    sat = SAT(problem, solution, threshold=.35, iteration_limit=200000)
    solution = sat.walk_sat()
    print(solution)
    print('\n')

if __name__ == '__main__':
    #-- Feel Free to run which ever test you like. Commented a few out for ease of use.
    #test1()
    #test2()
    #test3()
    #test4()
    #test5()
    t1 = time.time()
    test6()
    t2 = time.time()
    print('Time: %d' % (t2-t1,))
   # test11()
    #test12()
    #test13()
    #test14()
