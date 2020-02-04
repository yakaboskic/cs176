import time
import sys
import random
import copy
from display import display_sudoku_solution

'''
Solution class that does bookeeping, printing and retainment of assignment throughout the solving process.
'''
class GenericSolution:
    def __init__(self, sat_problem):
        self.iterations = 0
        self.threshold = None
        self.sat_problem = sat_problem
        self.avg_loop_time = None
        self.start_time = time.time()
        self.total_runtime = -1
        self.analysis_type = None
        self.problem_name = sat_problem.problem_name
        #-- Initialize a random assignment
        self.assignment = []
        for i in range(1, len(sat_problem.problem_variables) + 1):
            r = random.random()
            if r <= .5:
                self.assignment.append(i)
            else:
                self.assignment.append(-i)

    def write_solution(self):
        with open(self.sat_problem.solution_filename, 'w') as sol:
            for assignment in self.assignment:
                if assignment < 0:
                    sol.write(str(-self.sat_problem.map[abs(assignment)]))
                    sol.write('\n')
                else:
                    sol.write(str(self.sat_problem.map[assignment]))
                    sol.write('\n')


''' Solver class. Can run GSAT or WalkSAT.'''
class SAT:
    def __init__(self, sat_problem, solution_obj, threshold=.3, iteration_limit=100000):
        self.sat_problem = sat_problem
        self.threshold = threshold
        self.iteration_limit = iteration_limit
        self.solution = solution_obj
        self.solution.threshold = threshold
        self.unsatisfied = -1
        #-- Preprocessing step: Map to clauses that only involve the given variable.
        self.var_to_clause_map = {var:[clause for clause in self.sat_problem.clauses
                                       for literal in clause 
                                       if abs(literal) - 1 == var] 
                                  for var in range(0, len(self.sat_problem.problem_variables))}
        #print(self.var_to_clause_map[0])

    def write_solution(self):
        self.solution.write_solution()

    '''
    GSAT Implementation:
    '''
    def gsat(self):
        self.solution.analysis_type = 'GSAT'

        while not self.is_satisfied() and self.solution.iterations < self.iteration_limit:
            t_start = time.time()
            r = random.random()

            #-- If random number is less than threshold flip a random assignment.
            if r < self.threshold:
                var_choice = random.randrange(0, len(self.solution.assignment))
                self.solution.assignment[var_choice] = -1 * self.solution.assignment[var_choice]
            else:
                #-- Score and sort each variable.
                #-- Build a list of maximum scoring variables
                max_score = -1
                best_variables = []
                for var in range(0, len(self.solution.assignment)):
                    score = self.get_score(var)
                    if score > max_score:
                        max_score = score
                        best_variables = [var]
                    elif score == max_score:
                        best_variables.append(var)

                #-- Choose a random variable with the best score.
                var_to_flip = random.choice(best_variables)
                self.solution.assignment[var_to_flip] = -1 * self.solution.assignment[var_to_flip]

            #-- Bookkeeping and Display
            self.solution.iterations += 1
            self.display_status(t_start)

        self.solution.total_runtime = time.time() - self.solution.start_time
        return self.solution

    '''
    WalkSAT Implementation:
    '''
    def walk_sat(self):
        self.solution.analysis_type = 'WalkSAT'

        while not self.is_satisfied() and self.solution.iterations < self.iteration_limit:
            t_start = time.time()
            r = random.random()
            rand_clause = self.get_random_unsatisfied_clause_slow()
            var_candidates = [abs(literal) - 1 for literal in rand_clause]

            #-- Execute GSAT Step every now and then.
            if r < .05:
                var_choice = random.randrange(0, len(self.solution.assignment))
                self.solution.assignment[var_choice] = -1 * self.solution.assignment[var_choice]
                #print('<<', var_choice)

            #-- If random number is greater than threshold flip a random assignment.
            elif r >= .05 and r < self.threshold:
                var_choice = random.choice(var_candidates)
                self.solution.assignment[var_choice] = -1 * self.solution.assignment[var_choice]

            else:
                #-- Score and sort each variable.
                #-- Build a list of maximum scoring variables
                max_score = -1
                best_variables = []

                for var in var_candidates:
                    score = self.get_score(var)
                    if score > max_score:
                        max_score = score
                        best_variables = [var]
                    elif score == max_score:
                        best_variables.append(var)

                #-- Choose a random variable with the best score.
                var_to_flip = random.choice(best_variables)
                self.solution.assignment[var_to_flip] = -1 * self.solution.assignment[var_to_flip]

            #-- Bookeeping and Display Stuff.
            self.solution.iterations += 1
            self.display_status(t_start)

        #-- If there is no solution and we've reached the iteration limit print the unsatisfied clauses.
        if self.solution.iterations >= self.iteration_limit:
            unsatisfied = self.get_unsatisfied_clauses()
            print('\nUnsatisfied Clauses:')
            for clause in unsatisfied:
                origin_clause = []
                for literal in clause:
                    if literal < 0:
                        origin_clause.append(-self.sat_problem.map[abs(literal)])
                    else:
                        origin_clause.append(self.sat_problem.map[literal])
                print(origin_clause)

        self.solution.total_runtime = time.time() - self.solution.start_time
        return self.solution


    ''' All other functions are helper functions. There purpose should be self explainatory. '''


    '''
    Here we choose a random clause to start our unsatisfied clause loop search. 
    This way we don't have to go through every clause each time and still maintain randomness.
    '''
    def get_random_unsatisfied_clause_fast(self):
        clause = None
        start_ind = random.randrange(0, len(self.sat_problem.clauses))
        for i in range(start_ind, len(self.sat_problem.clauses)):
            clause = self.sat_problem.clauses[i]
            if not self.clause_satisfied(clause, self.solution.assignment):
                return clause
        for j in range(0, start_ind):
            clause = self.sat_problem.clauses[j]
            if not self.clause_satisfied(clause, self.solution.assignment):
                return clause
        return None

    def get_unsatisfied_clauses(self):
        unsatisfied = []
        for clause in self.sat_problem.clauses:
            if not self.clause_satisfied(clause, self.solution.assignment):
                unsatisfied.append(clause)
        return unsatisfied

    def get_random_unsatisfied_clause_slow(self):
        unsatisfied = self.get_unsatisfied_clauses()
        self.unsatisfied = len(unsatisfied)
        return random.choice(unsatisfied)

    def get_variables_of_unsatisfied_clauses(self):
        candidates = set()
        for clause in self.sat_problem.clauses:
            if not self.clause_satisfied(clause, self.solution.assignment):
                for literal in clause:
                    #-- Subtract one cause we want variable indices
                    candidates.add(abs(literal) - 1)
        return candidates

    def get_score(self, var):
        assignment = copy.deepcopy(self.solution.assignment)
        assignment[var] = -1 * assignment[var]

        count = 0
        for clause in self.sat_problem.clauses:
            if self.clause_satisfied(clause, assignment):
                count += 1
        return count

    def is_satisfied(self):
        for clause in self.sat_problem.clauses:
            if not self.clause_satisfied(clause, self.solution.assignment):
                return False
        return True

    def clause_satisfied(self, clause, assignment):
        for literal in clause:
            if literal == assignment[abs(literal) - 1]:
                return True
        return False

    '''
    Method that displays current progress of solver.
    '''
    def display_status(self, t):
        if self.solution.avg_loop_time is None:
            self.solution.avg_loop_time = time.time() - t
        else:
            loop_time = time.time() - t
            self.solution.avg_loop_time = (loop_time + self.solution.avg_loop_time)/2
        sys.stdout.write('\r')
        sys.stdout.write('Current Iteration: %s | # Unsatisfied: %s | Average Loop Time: %.5f sec'  % (self.solution.iterations, 
                                                                                                 self.unsatisfied, self.solution.avg_loop_time))
        sys.stdout.flush()
