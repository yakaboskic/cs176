from mazeworld.Maze import Maze
from Problems import RobotProblem, UmbrellaProblem
from HMM import HMM


def test_0():
    print('---------- Test 0: Umbrella World -------------')
    umbrella_problem = UmbrellaProblem()
    hmm = HMM(umbrella_problem)
    solution = hmm.forward_backward([int(obs) for obs in [True, True]])
    print(solution)
    print('Forward Updates:')
    print(solution.updates)
    print('Backward Updates:')
    print(solution.updates_smoothed)


def test_1():
    '''
    Straight 4x1 maze test with deterministic sensor. Given the evidence RED, GREEN, BLUE, YELLOW we should know exactly where we are
    since there is no other sequence to yeild that evidence other than starting at (0,0) and traveling east, east, east. 
    '''
    print('---------- Test 1: Deterministic Simple Robot Maze-------------')
    robot_problem = RobotProblem('maze_straight.maz', deterministic_sensor=True)
    hmm = HMM(robot_problem)
    solution = hmm.reason([0,2,1,3])
    print(solution)

def test_2():
    '''
    Same problem as in test_1 but using normal noisy sensor, should still have the highest probability of being in (3,0) at the end but with other lower
    probabilities as well. 
    '''
    print('----------- Test 2: Noisy Sensor in Simple Robot Maze. -----------')
    robot_problem = RobotProblem('maze_straight.maz', deterministic_sensor=False)
    hmm = HMM(robot_problem)
    solution = hmm.reason([0,2,1,3])
    print(solution)


def test_3():
    print('------------ Test 3: 4x4 Colored Maze with Noisy Sensor. ----------------')
    path = [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)]
    robot_problem = RobotProblem('maze1.maz', deterministic_sensor=False)
    ground_truth = robot_problem.get_ground_truth(path)
    print('Path: ', ' -> '.join(['(%s, %s)' % (state[0], state[1]) for state in path]))
    print('Ground Truth: ', ' -> '.join([robot_problem.color_map[i] for i in ground_truth]))
    hmm = HMM(robot_problem)
    solution = hmm.forward_backward(ground_truth)
    print(solution)
    print('-------- Path Animation ----------')
    robot_problem.animate_path(path, solution)



if __name__ == '__main__':
    test_0()
    test_1()
    test_2()
    test_3()
