import itertools
import copy


class ConstraintSatisfactionProblem:
    def __init__(self, variables, domains, neighbors, constraints=None):
        self.number_of_variables = len(variables)

        #-- Get all the domain values in the problem.
        self.set_of_domains = set([domain for var in variables for domain in domains[var]])

        #-- Create maps to and from problem variables.
        self.map_domains = {i: domain for i, domain in enumerate(self.set_of_domains)}
        self.inverse_map_domains = {v: k for k, v in self.map_domains.items()}
        self.map_variables = {i: var for i, var in enumerate(variables)}
        self.inverse_map_variables = {v: k for k, v in self.map_variables.items()}

        #-- Map Constraints to Integer values
        self.constraints = dict()
        for arc in constraints:
            self.constraints[(self.inverse_map_variables[arc[0]], self.inverse_map_variables[arc[1]])] = set()
            for constraint in constraints[arc]:
                self.constraints[(self.inverse_map_variables[arc[0]], self.inverse_map_variables[arc[1]])].add(
                    (self.inverse_map_domains[constraint[0]], self.inverse_map_domains[constraint[1]]))

        #-- Map variables, domains and neighbors to integer values.
        self.variables = set(range(self.number_of_variables))
        self.domains = {i: set([self.inverse_map_domains[domain] for domain in domains[var]]) for i, var in enumerate(variables)}
        self.neighbors = {self.inverse_map_variables[var]: [self.inverse_map_variables[neighbor] for neighbor in neighbors[var]] for var in variables}

        #-- Handle Flags
        self.curr_domains = None
        self.mrv = False
        self.lcv = False

    #-- Check if complete
    def is_complete(self, assignment):
        return len(assignment) == self.number_of_variables

    #-- Get unassigned variables 
    def get_unassigned_variable(self, assignment):
        assigned_variables = set([var for var, value in assignment])
        unassigned_variables = self.variables.difference(assigned_variables)

        #-- Using Minimum Remaining Value Hueristic
        if self.mrv:
            mrv_sorted_variables = []
            for var in unassigned_variables:
                mrv_sorted_variables.append((self.get_num_legal_values(var, assignment), var))
            mrv_sorted_variables = sorted(mrv_sorted_variables)

            #-- Return the variable in the first sorted tuple.
            return mrv_sorted_variables[0][1]

        #-- If no heuristic just return first variable.
        else:
            return unassigned_variables.pop()

    #-- Get the number of legal states. Used with MRV.
    def get_num_legal_values(self, var, assignment):
        #-- Start with all the legal states
        num_legal_values = len(self.domains[var])

        #-- Iterate though each possible value of the variable
        for value in self.domains[var]:
            #-- If there was a conflict between a variable value and the current assignment decease the number of legal states by one.
            if self.get_num_conflicts(var, value, assignment) != 0:
                num_legal_values -= 1

        return num_legal_values

    #-- Get the number of conflicts from a specific variable assignment.
    def get_num_conflicts(self, var, value, assignment):
        count = 0

        #-- For each variable in the assignment
        for ass_var, ass_value in assignment:
            #-- Check if that variable is a neighbor of the variable under question
            if ass_var in set(self.neighbors[var]):
                #-- See if there is a conflict in constraints and if so increase the count
                if (ass_value, value) not in self.constraints[(ass_var, var)]:
                    count += 1
        return count

    def order_domain_values(self, var, assignment):
        #-- If using LCV
        if self.lcv:
            lcv_sorted_values = []
            #-- Sort by least number of conflicts
            for value in self.domains[var]:
                lcv_sorted_values.append((self.get_num_conflicts(var, value, assignment), value))
            lcv_sorted_values = sorted(lcv_sorted_values)
            sorted_domain = [x[1] for x in lcv_sorted_values]
            return sorted_domain

        #-- Else just return the domain of the variable in any order
        else:
            return self.domains[var]

    def is_consistent(self, var, value, assignment):
        #-- If there is an incosistency found return False
        for constraint in self.constraints:
            for ass_var, ass_value in assignment:
                if var == constraint[0] and ass_var == constraint[1]:
                    if (value, ass_value) not in self.constraints[constraint]:
                        return False
        return True

    #-- Conducts an AC-3 and returns inferences based on remaining domains.
    def get_inferences(self, var, value, assignment):
        #-- If using MAC
        if self.curr_domains is not None:
            #-- copy the domains and put into current domains.
            self.curr_domains = copy.deepcopy(self.domains)

            #-- Get unassigned variables
            unassigned = self.variables.difference(set([variable for variable, value in assignment]))
            #-- And build queue with only neighbors of the variable of interest.
            queue = set([(var, neighbor) for neighbor in self.neighbors[var] if neighbor in unassigned])

            #-- Run AC-3
            if self.arc_consistency_3(queue):
                inferences = set([(x, list(self.curr_domains[x])[0]) for x in unassigned - {var}])
                return inferences
            else:
                #-- return None only if AC fails, i.e. a current domain gets reduced to zero. Else just return an empty set of no inferences are made.
                return None

        #-- If not using MAC-3, just return an empty set.
        return set()

    #-- AC-3 follows pseudo-code in the book.
    def arc_consistency_3(self, queue=None):
        if queue is None:
            queue = set([arc for arc in self.constraints])
        while len(queue) > 0:
            arc = queue.pop()
            #print(arc)
            if self.revise(arc):
                if len(self.curr_domains[arc[0]]) == 0:
                    return False
                for neighbor in set(self.neighbors[arc[0]]) - {arc[1]}:
                    queue.add((neighbor, arc[0]))
        return True

    def revise(self, arc):
        revised = False
        curr_domains_x = copy.deepcopy(self.curr_domains[arc[0]])
        for x in curr_domains_x:
            found = False
            for y in self.curr_domains[arc[1]]:
                if (x, y) in self.constraints[arc]:
                    found = True
                    break
            if not found:
                self.curr_domains[arc[0]].remove(x)
                revised = True
        return revised

    def __str__(self):
        string = ''

        string += 'Variable Map = %s\n' % self.map_variables
        string += 'Domain Map = %s\n' % self.map_domains

        string += 'Constraint Matrix =\n'
        for pair in self.constraints:
            string += '\t %s => %s\n' % (pair, self.constraints[pair])
        string += '\n'
        for pair in self.constraints:
            string += '\t (%s, %s) \t => {' % (self.map_variables[pair[0]], self.map_variables[pair[1]])
            for constraint in self.constraints[pair]:
                string += ' (%s, %s) ' % (self.map_domains[constraint[0]], self.map_domains[constraint[1]])
            string += '}\n'

        return string
