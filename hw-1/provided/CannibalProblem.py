import itertools

class CannibalProblem:
    #-- State Description: (Number of Missionaries, Number of Cannibals, Boat State) on the start side.
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.total_missionaries = self.start_state[0]
        self.total_cannibals = self.start_state[1]
        # you might want to add other things to the problem,
        #  like the total number of missionaries (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        #-- If the boat is on the start side then we can only send people across to the goal side.
        successor_list = []
        if state[2] == 1:
            for successor in itertools.product(range(state[0]-2, state[0]+1), range(state[1]-2, state[1]+1)):
                if self.test_successor(state, successor) == True:
                    successor_list.append(successor + (0,))
                else:
                    continue

        #-- If the boat is on the goal side we can only get the boat back with people on it.
        else:
            for successor in itertools.product(range(state[0], state[0]+3), range(state[1], state[1]+3)):
                if self.test_successor(state, successor) == True:
                    successor_list.append(successor + (1,))
                else:
                    continue
        return successor_list


        # you write this part. I also had a helper function
        #  that tested if states were safe before adding to successor list

    # I also had a goal test method. You should write one.
    def goal_test(self, state):
        if state == self.goal_state:
            return True
        else:
            return False

    def test_successor(self, current_state, successor):
        if current_state[0:2] != successor:
            #-- Make sure the number missionaries and cannibals are with in scope.
            if successor[0] >= 0 and successor[1] >= 0 and successor[0] <= self.total_missionaries and successor[1] <= self.total_cannibals:
                #-- Make sure the Cannibals don't out number the missionaries on the start side or are left alone.
                if successor[0] >= successor[1] or successor[0] == 0:
                    #-- Make sure the Cannibals don't out number the missionaries on the goal side or are left alone.
                    if self.total_missionaries - successor[0] >= self.total_cannibals - successor[1] or self.total_missionaries - successor[0] == 0:
                            #-- Make sure the number of the people in the boat does not exceed two.
                            if current_state[0] - successor[0] + current_state[1] - successor[1] <= 2:
                                return True
        return False

    def __str__(self):
        string =  "Missionaries and cannibals problem: " + str(self.start_state)
        return string

    def run(self):
        self.__str__()
        print('Press "q" to quit.')
        new_state = self.start_state
        action = None
        while action != 'q':
            successors = self.get_successors(new_state)
            print('Choose your next state:')
            for i, successor in enumerate(successors):
                print(str(i) + ':', successor)
            action = srt(input())
            if action == 'q':
                break
            new_state = successors[int(action)]
            if new_state == self.goal_state:
                print('Congrats!')
                action = 'q'

## A bit of test code

if __name__ == "__main__":
    test_cp = CannibalProblem((3, 3, 1))
    test_cp.run()
    #print(test_cp.get_successors((2, 2, 0)))
    #print(test_cp)
