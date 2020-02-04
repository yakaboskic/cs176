from Sudoku import Sudoku
from display import display_sudoku_solution
from GenericProblem import GenericSatProblem
import itertools
from SAT import GenericSolution

class SudokuProblem(GenericSatProblem):
    def __init__(self, file_name, cnf_filename=None):
        if cnf_filename is None:
            #-- Set up and load in puzzle
            self.sudoku = Sudoku()
            self.puzzle_name = str(file_name[:-4])
            self.solution_filename = self.puzzle_name + ".sol"
            self.cnf_filename = self.puzzle_name + ".cnf"

            self.sudoku.load(file_name)
            self.sudoku.generate_cnf(self.cnf_filename)

        else:
            self.puzzle_name = str(file_name[:-4])
            self.solution_filename = self.puzzle_name + ".sol"
            self.cnf_filename = cnf_filename

        #-- Load in clauses
        clauses = []
        with open(self.cnf_filename, 'r') as cnf:
            lines = cnf.readlines()
        for line in lines:
            clause = list(map(int, line.rstrip('\n').strip().split(' ')))
            clauses.append(clause)

        #-- Make sudoku variables
        variables = [int(''.join(str(x) for x in var)) for var in itertools.product(range(1,10), repeat=3)]

        #-- Set up generic class
        super().__init__(variables, clauses, problem_name='Sudoku')


class SudokuSolution(GenericSolution):
    def __init__(self, sudoku_problem):
        super().__init__(sudoku_problem)

    def __str__(self):
        print('\n')
        self.write_solution()
        string = ''
        string += '^^------%s with %s Solution------^^\n\n' % (self.problem_name, self.analysis_type)
        string += 'Threshold: %s \nIterations: %s \nRuntime: %s\nAverage Loop Runtime: %s' % (self.threshold, self.iterations, 
                                                                                              self.total_runtime, self.avg_loop_time)
        print('Sudoku Solution Board:\n')
        display_sudoku_solution(self.sat_problem.solution_filename)
        return string
