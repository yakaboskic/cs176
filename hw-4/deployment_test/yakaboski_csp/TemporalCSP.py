from csp import ConstraintSatisfactionProblem as csp
import itertools

class TemporalCSP(csp):
    def __init__(self):

        #-- This is the John and Fred Problem described in the report.
        time_scope = range(0, 100)
        variables = {'J Leaves Home', 'J Arrives at Work', 'F Leaves Home', 'F Arrives at Work'}
        domains = {var: set([time for time in time_scope]) for var in variables}

        #-- Update a few restricted domains
        domains['J Leaves Home'] = set([time for time in range(10,21)])
        domains['F Arrived at Work'] = set([time for time in range(60,71)])

        neighbors = {var: [other_var for other_var in variables - {var}] for var in variables}
        constraints = {pair: Get_Constraints(pair[0], domains[pair[0]], pair[1], domains[pair[1]]) for pair in itertools.permutations(variables)}

        #-- Set up the General CSP with the map coloring parameters using inherentance
        super().__init__(variables, domains, neighbors, constraints)

    #-- Printer Function
    def print_assignment(self, assignment):
        string = 'Assignment = {'
        for partial in assignment:
            string += ' (%s, %s) ' % (self.map_variables[partial[0]], self.map_domains[partial[1]])
        string += '}'
        return string


#-- Calculates legal times for each pairwise events. The constraints are detailed in the report. Fast and dirty implementation. 
def Get_Constraints(event1, domains1, event2, domains2):
    #-- Constraint: 30 <= X_2 - X_1 <= 40 or  X_4 - X_3 >= 60
    if event1 == 'J Leaves Home' and event2 == 'J Arrives at Work':
        legal_values = []
        for x2 in domains2:
            for x1 in domains1:
                if (x2 - x1 <= 40 and x2 - x1 >= 30) or x2 - x1 >= 60 :
                    legal_values.append((x1, x2))
        return set(legal_values)
    if event2 == 'J Leaves Home' and event1 == 'J Arrives at Work':
        legal_values = []
        for x2 in domains2:
            for x1 in domains1:
                if (x2 - x1 >= -40 and x2 - x1 <= -30) or x2 - x1 <= -60:
                    legal_values.append((x1, x2))
        return set(legal_values)

    #-- Constraint: 20 <= X_4 - X_3 <= 30 or 40 <= X_4 - X_3 <= 50
    if event1 == 'F Leaves Home' and event2 == 'F Arrives at Work':
        legal_values = []
        for x2 in domains2:
            for x1 in domains1:
                if (x2 - x1 <= 30 and x2 - x1 >= 20) or (x2 - x1 >= 40 and x2 - x1 <= 50):
                    legal_values.append((x1, x2))
        return set(legal_values)
    if event2 == 'F Leaves Home' and event1 == 'F Arrives at Work':
        legal_values = []
        for x2 in domains2:
            for x1 in domains1:
                if (x2 - x1 >= -30 and x2 - x1 <= -20) or (x2 - x1 <= -40 and x2 - x1 >= -50):
                    legal_values.append((x1, x2))
        return set(legal_values)

    #-- Constraint: 10 <= X_2 - X_3 <= 20
    if event1 == 'J Arrives at Work' and event2 == 'F Leaves Home':
        legal_values = []
        for x2 in domains2:
            for x1 in domains1:
                if (x2 - x1 <= 20 and x2 - x1 >= 10):
                    legal_values.append((x1, x2))
        return set(legal_values)
    if event2 == 'J Arrives at Work' and event1 == 'F Leaves Home':
        legal_values = []
        for x2 in domains2:
            for x1 in domains1:
                if (x2 - x1 >= -20 and x2 - x1 <= -10):
                    legal_values.append((x1, x2))
        return set(legal_values)

#-- Else return all time point pairs
    legal_values = []
    for x1 in domains1:
        for x2 in domains2:
            legal_values.append((x1,x2))
    return set(legal_values)
