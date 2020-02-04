from GenericProblem import GenericSatProblem
from SAT import GenericSolution
import itertools

class MapColoringProblem(GenericSatProblem):
    def __init__(self, cnf_filename):
        #-- Set up Australian variables, domains and constraints
        self.mcp_labels = ('WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T')
        self.domain_labels = ['r', 'g', 'b']
        self.label_map = {i+1: label for i, label in enumerate(self.mcp_labels)}
        self.label_inverse_map = {label: j for j, label in self.label_map.items()}
        self.cnf_filename = cnf_filename
        self.puzzle_name = str(cnf_filename[:-4])
        self.solution_filename = self.puzzle_name + ".sol"

        #-- Load in clauses
        variables = set()
        clauses = []
        with open(self.cnf_filename, 'r') as cnf:
            lines = cnf.readlines()
        for line in lines:
            clause = list(map(int, line.rstrip('\n').strip().split(' ')))
            clauses.append(clause)
            for literal in clause:
                variables.add(abs(literal))

        #-- Set up generic class
        super().__init__(variables, clauses, problem_name='Map Coloring')


class MapColoringSolution(GenericSolution):
    def __init__(self, mapColoring_problem):
        super().__init__(mapColoring_problem)

    def __str__(self):
        print('\n')
        self.write_solution()
        string = ''
        string += '------%s with %s Solution------\n\n' % (self.problem_name, self.analysis_type)
        true_ass = []
        with open(self.sat_problem.solution_filename) as sol_file:
            lines = sol_file.readlines()
            for line in lines:
                literal = int(line)
                if literal > 0:
                    true_ass.append(literal)

        string += 'Assignment:\n'
        for literal in true_ass:
            string += str((self.sat_problem.label_map[int(str(literal)[0])], self.sat_problem.domain_labels[int(str(literal)[1]) - 1]))
        string += '\n'

        string += 'Threshold: %s \nIterations: %s \nRuntime: %s\nAverage Loop Runtime: %s' % (self.threshold, self.iterations, 
                                                                                              self.total_runtime, self.avg_loop_time)
        return string
