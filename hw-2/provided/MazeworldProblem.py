from Maze import Maze
from time import sleep
import itertools

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = tuple(maze.robotloc)
        self.number_of_robots = len(self.start_state)/2

    def goal_test(self, locations):
       if self.goal_locations == locations:
           return True
       else:
           return False

    def get_successors(self, locations):
        successors = []
        potential_action_vectors = [(1,0), (0,1), (-1,0), (0,-1)]
        for action in potential_action_vectors:
            for robot_loc in range(0, len(self.start_state), 2):
                new_location = (locations[robot_loc] + action[0], locations[robot_loc + 1] + action[1])
                if self.maze.is_floor(new_location[0], new_location[1]) and not self.is_collision(locations, new_location):
                    new_state = list(locations)
                    new_state[robot_loc] = new_location[0]
                    new_state[robot_loc + 1] = new_location[1]
                    successors.append(tuple(new_state))
        return successors

    def is_collision(self, locations, new_location):
        for robot_loc in range(0, len(self.start_state), 2):
            if locations[robot_loc] == new_location[0] and locations[robot_loc + 1] == new_location[1]:
                return True
        return False

    def __str__(self):
        string =  "Mazeworld problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))

    def manhattan_heuristic(self, state):
        sum_ = 0
        for ind in range(len(state)):
            sum_ += abs(self.goal_locations[ind] - state[ind])
        return sum_

    
    # null heuristic, useful for testing astar search without heuristic (uniform cost search).
    def null_heuristic(self, state):
        return 0

## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
