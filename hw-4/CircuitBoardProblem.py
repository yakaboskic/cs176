from csp import ConstraintSatisfactionProblem as csp
import itertools

class CircuitBoardProblem(csp):
    def __init__(self, board, circuits):
        self.board = board
        self.cbp_variables = tuple(circuits)
        self.cbp_domains = {var: Find_Domain(var, self.board) for var in self.cbp_variables}

        #-- Check the Domains if you want. Just Uncomment.
        #print('Domains Test-----')
        #for var in self.cbp_variables:
        #    print('Chip: %s' % var.letter, '=>', self.cbp_domains[var])

        self.cbp_neighbors = {var: [other_var for other_var in set(self.cbp_variables) - {var}] for var in self.cbp_variables}
        self.cbp_constraints = {arc: Get_Constraints(arc[0], self.cbp_domains[arc[0]], arc[1], self.cbp_domains[arc[1]]) for arc in itertools.permutations(self.cbp_variables, r=2)}

        #-- Check the Constraints if you want. Just Uncomment.
        #print('Constraint Test ---')
        #print(circuit_a, 'and', circuit_b)
        #print(Get_Constraints(circuit_a, self.cbp_domains[circuit_a], circuit_b, self.cbp_domains[circuit_b]))

        #-- Set up the General CSP with the map coloring parameters using inherentance
        super().__init__(self.cbp_variables, self.cbp_domains, self.cbp_neighbors, self.cbp_constraints)

    #-- Printer Function
    def print_assignment(self, assignment):
        string = 'Assignment = {'
        for partial in assignment:
            string += ' (%s, %s) ' % (self.map_variables[partial[0]], self.map_domains[partial[1]])
        string += '}'

        #-- Print Board
        for partial in assignment:
            self.board.place_chip(self.map_variables[partial[0]], self.map_domains[partial[1]])
        string += self.board.__str__()
        return string

#-- Gets the allowable placements on the board so that the circuit won't go over. 
def Find_Domain(circuit, board):
    domain = []
    for x in range(0, board.n - circuit.w + 1):
        for y in range(0, board.m - circuit.h + 1):
            domain.append((x,y))
    return set(domain)

#-- Get's legal circuit positions between two circuits.
def Get_Constraints(circuit_1, domain_1, circuit_2, domain_2):
    legal_states = []
    for location1 in domain_1:
        for location2 in domain_2:
            if BinaryCircuitConstraint(circuit_1, location1, circuit_2, location2):
                legal_states.append((location1, location2))
    return set(legal_states)

#-- Returns True if two chips DO NOT overlap, and False if they do.
def BinaryCircuitConstraint(circuit1, location1, circuit2, location2):
    #-- Left bottom edge of the first chip
    lb1 = location1
    #-- Right edge location of the first chip
    rt1 = (location1[0] + circuit1.w - 1, location1[1] + circuit1.h - 1)

    #-- Left bottom edge of the second chip
    lb2 = location2
    #-- Right edge location of the second chip
    rt2 = (location2[0] + circuit2.w - 1, location2[1] + circuit2.h - 1)

    if rt1[0] < lb2[0] or rt2[0] < lb1[0]:
        return True

    if rt1[1] < lb2[1] or rt2[1] < lb1[1]:
        return True
    return False


#-- Circuit Helper Class
class Circuit:
    def __init__(self, width, height, letter_rep='a'):
        self.w = width
        self.h = height
        self.letter = letter_rep

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return 'Circuit: %s' % self.letter


#-- Circuit Board Helper Class
class CircuitBoard:
    def __init__(self, n, m, chips=None):
        self.n = n
        self.m = m
        if chips is None:
            self.chips = dict()
        else:
            self.chips = chips

    def place_chip(self, chip, location):
        self.chips[chip] = location

    def get_index(self, x, y):
        return (self.m - y - 1)*self.n + x

    def __str__(self):
        render_list = ['.' for _ in range(self.n*self.m)]
        for chip in self.chips:
            start_location = (self.chips[chip][0], self.chips[chip][1] + chip.h - 1)
            #-- Fill in the circuit with its letter representation
            for i in range(chip.h - 1, -1, -1):
                for j in range(0, chip.w):
                    idx = self.get_index(start_location[0] + j, start_location[1] - i)
                    if idx >= 0 and idx <= self.m*self.n:
                        render_list[idx] = chip.letter

        string = '\nBoard Layout:'
        for i, value in enumerate(render_list):
            if i%self.n == 0:
                string += '\n\t'
            string += value
        return string

