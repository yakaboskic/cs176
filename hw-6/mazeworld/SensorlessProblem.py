from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze, goal_location):
        self.maze = maze
        self.goal_location = goal_location
        self.start_state = self.get_start_state()

    def get_start_state(self):
        start_state = set()
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x,y):
                    start_state.add((x,y))
        return tuple(start_state)

    def goal_test(self, state):
        if len(state) != 1:
            return False
        else:
            if self.goal_location == state[0]:
                return True
            else:
                return False

    def get_successors(self, state):
        successors = []
        action_vectors = [(1,0), (-1,0), (0,1), (0,-1)]
        for action in action_vectors:
            new_state = set()
            for location in state:
                new_location = (location[0] + action[0], location[1] + action[1])
                if self.maze.is_floor(new_location[0], new_location[1]):
                    new_state.add(new_location)
                else:
                    new_state.add(location)
            successors.append(tuple(new_state))
        return successors

    def get_actions_from_path(self, path):
        actions = []
        action_vectors = [(1,0), (-1,0), (0,1), (0,-1)]
        action_map = {(1,0): 'East', (-1,0): 'West', (0,1): 'North', (0,-1): 'South'}
        for i in range(len(path) - 1):
            for action in action_vectors:
                next_state = set()
                for location in path[i]:
                    new_location = (location[0] + action[0], location[1] + action[1])
                    if self.maze.is_floor(new_location[0], new_location[1]):
                        next_state.add((new_location[0], new_location[1]))
                    else:
                        next_state.add(location)
                if next_state == set(path[i + 1]):
                    actions.append(action)
        return [action_map[action] for action in actions]

    def __str__(self):
        string =  "Blind robot problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.blindstate = tuple(state)
            sleep(1)

            print(str(self.maze))

    def manhattan_heuristic(self, state):
        sum_ = 0
        for location in state:
            for ind in range(len(location)):
                sum_ += abs(self.goal_location[ind] - location[ind])
        return sum_

    def cardinality_heuristic(self, state):
        return len(state)


    # null heuristic, useful for testing astar search without heuristic (uniform cost search).
    def null_heuristic(self, state):
        return 0


## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
