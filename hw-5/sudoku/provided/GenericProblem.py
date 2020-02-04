


class GenericSatProblem:
    def __init__(self, problem_variables, problem_clauses, problem_name='User_Problem'):
        self.problem_variables = problem_variables
        self.problem_clauses = problem_clauses
        self.problem_name = problem_name

        #-- maps to/from problem variables
        self.map = {i+1: var for i, var in enumerate(self.problem_variables)}
        self.inverse_map = {var: i for i, var in self.map.items()}

        #-- Set up generic variable clauses
        self.clauses = []
        for problem_clause in self.problem_clauses:
            clause = []
            for literal in problem_clause:
                if literal < 0:
                    clause.append(-self.inverse_map[abs(literal)])
                else:
                    clause.append(self.inverse_map[abs(literal)])
            self.clauses.append(clause)
        #print(self.map)
        #print(self.clauses)
