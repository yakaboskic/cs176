

class SearchSolution:
    def __init__(self, search_problem):
        self.assignment = set()
        self.num_of_assigns = 0
        self.search_problem = search_problem
        self.no_solution = False

    def __str__(self):
        if self.no_solution:
            string = 'Search Solution: No Solution Found\n'
            string += 'Number of Calls to Backtrack = %s' % self.num_of_assigns
            return string

        string = 'Search Solution:\n'
        string += self.search_problem.print_assignment(self.assignment)
        string += '\n'
        string += 'Number of Calls to Backtrack = %s' % self.num_of_assigns
        return string


def backtracking_search(search_problem, mac=False, mrv=False, lcv=False):
    #-- Check flags
    if mac:
        search_problem.curr_domains = set()
    if mrv:
        search_problem.mrv = True
    if lcv:
        search_problem.lcv = True

    #-- Get the solution
    solution = SearchSolution(search_problem)
    solution = backtrack(solution, search_problem)
    return solution


def backtrack(solution, search_problem):
    #-- If we found a solution
    if search_problem.is_complete(solution.assignment):
        solution.no_solution = False
        return solution

    #-- Get the next variable not already assigned.
    var = search_problem.get_unassigned_variable(solution.assignment)
    solution.num_of_assigns += 1

    #-- For each potential value that variable can take...
    for value in search_problem.order_domain_values(var, solution.assignment):
        #-- Check if it is consistent and add to the assignment if so.
        if search_problem.is_consistent(var, value, solution.assignment):
            solution.assignment.add((var, value))

            #-- Get some inferences that can be made from this assignment and add them to the assignment
            inferences = search_problem.get_inferences(var, value, solution.assignment)

            #-- If Inferences did not fail
            if inferences is not None:
                for inference in inferences:
                    #-- Check if inference is consistent
                    if search_problem.is_consistent(inference[0], inference[1], solution.assignment):
                        solution.assignment.add(inference)

                result = backtrack(solution, search_problem)
                if not result.no_solution:
                    return result

            #-- Undo current assignment
            solution.assignment.remove((var, value))

            #-- Undo Inferences if we need to.
            if inferences is not None:
                for inference in inferences:
                    if inference in solution.assignment:
                        solution.assignment.remove(inference)

    solution.no_solution = True
    return solution
