from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        return self.transition_cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    # you write the rest:
    while len(pqueue) > 0:
        solution.nodes_visited += 1
        node = heappop(pqueue)
        if search_problem.goal_test(node.state):
            solution.path = backchain(node)
            solution.cost = visited_cost[node.state]
            return solution
        for next_state in search_problem.get_successors(node.state):
            next_node = AstarNode(next_state, heuristic_fn, parent=node, 
                                  transition_cost=heuristic_fn(next_state))
            if next_node.state not in visited_cost.keys():
                next_node_total_cost = visited_cost[node.state] + next_node.transition_cost
                visited_cost[next_node.state] = next_node_total_cost
                heappush(pqueue, next_node)
    return solution
