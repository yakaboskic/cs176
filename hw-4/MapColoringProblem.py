from csp import ConstraintSatisfactionProblem as csp
import itertools

class MapColoringProblem(csp):
    def __init__(self):
        #-- Set up Australian variables, domains and constraints
        self.mcp_variables = ('WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T')
        self.mcp_domains = {var: {'r', 'g', 'b'} for var in self.mcp_variables}
        self.mcp_neighbors = {'WA':['NT', 'SA'], 
                      'SA':['WA', 'NT', 'Q', 'NSW', 'V'], 
                      'NT':['WA', 'SA', 'Q',],
                      'Q': ['NT', 'SA', 'NSW'],
                      'NSW':['Q', 'SA', 'V'], 
                      'V': ['NSW', 'SA'],
                      'T': []}
        self.mcp_constraints = {arc: {binary_constraint for binary_constraint in itertools.product(self.mcp_domains[arc[0]], self.mcp_domains[arc[1]]) 
                                if binary_constraint[0] != binary_constraint[1]} 
                                    for x in self.mcp_neighbors for arc in itertools.product([x], self.mcp_neighbors[x])}

        #-- Set up the General CSP with the map coloring parameters using inherentance
        super().__init__(self.mcp_variables, self.mcp_domains, self.mcp_neighbors, self.mcp_constraints)

    #-- Printer Function
    def print_assignment(self, assignment):
        string = 'Assignment = {'
        for partial in assignment:
            string += ' (%s, %s) ' % (self.map_variables[partial[0]], self.map_domains[partial[1]])
        string += '}'
        return string
