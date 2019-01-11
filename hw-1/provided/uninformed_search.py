
from collections import deque
from SearchSolution import SearchSolution

class SearchNode:

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

    def get_parent(self):
        return self.parent

    def __eq__(self, other):
        if self.state == other.state:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return str(self.state)

def bfs_search(search_problem):
    solution = SearchSolution(search_problem, "BFS")
    root_node = SearchNode(search_problem.start_state)
    visited, queue = set(), deque([root_node])
    while queue:
        #-- Pop node off beginning of Queue
        node = queue.popleft()
        #-- Check if we have reached our goal.
        if search_problem.goal_test(node.state):
            visited.add(node)
            break
        if node not in visited:
            visited.add(node)
            #-- Get Successor States
            successor_states = search_problem.get_successors(node.state)
            for successor_state in successor_states:
                child_node = SearchNode(successor_state, parent=node)
                queue.append(child_node)
    adj_mat = build_adj_mat(visited)
    solution.path = backchain(adj_mat, search_problem.start_state, search_problem.goal_state)
    return solution

def build_adj_mat(path):
    #-- Build dictionary
    adjacency_dict = {node.parent.state if node.parent is not None else 'root': set() for node in path}
    for node in path:
        if node.parent is None:
            adjacency_dict['root'].add(node.state)
        else:
            adjacency_dict[node.parent.state].add(node.state)
    return adjacency_dict

def backchain(graph, start, goal, path=[]):
    path = path + [start]
    if start == goal:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = backchain(graph, node, goal, path)
            if newpath: return newpath
    return None

def dfs_search(search_problem, depth_limit=100, node=None, solution=None, found=False):
    # if no node object given, create a new search from starting state
    if node is None:
        node = SearchNode(search_problem.start_state)
    if solution is None:
        solution = SearchSolution(search_problem, "DFS")

    #-- Add node to the solution path and increase nodes visited. 
    solution.path.append(node)
    solution.nodes_visited += 1

    #-- Make sure we haven't exceed our depth limit.
    if solution.nodes_visited >= depth_limit:
        return False
    #-- Test if we have found our goal
    if search_problem.goal_test(node.state):
        return True
    else:
        #-- Get all child states to search
        for successor in search_problem.get_successors(node.state):
            successor_node = SearchNode(successor, parent=node)
            #-- Path check
            if successor_node not in set(solution.path):
                #-- Recursive, Go Deeper
                found = dfs_search(search_problem, node=successor_node, solution=solution, found=found)
                #-- If solution is found and we are back at the root node, return the solution
                if found and node.parent is None:
                    adj_mat = build_adj_mat(solution.path)
                    solution.path = backchain(adj_mat, search_problem.start_state, search_problem.goal_state)
                    return solution
                #-- If we found the solution but are not at the root node, continue up the chain
                elif found:
                    return True
                #-- Else, keep searching
                else:
                    return False

def ids_search(search_problem, depth_limit=100):
    for i in range(depth_limit):
        solution = dfs_search(search_problem, depth_limit=i)
        if solution is not False:
            return solution


