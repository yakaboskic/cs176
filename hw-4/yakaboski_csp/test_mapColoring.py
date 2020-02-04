from MapColoringProblem import MapColoringProblem
from backtracking_search import backtracking_search

#-- Test 1: Only Backtracking in Map Problem, No heuristics or inferencing.
def test_1():
    print('Test 1: Map Coloring CSP with no heuristic or inferencing.----------------------------')
    mapColoringProblem = MapColoringProblem()
    print(mapColoringProblem)
    solution = backtracking_search(mapColoringProblem)
    print(solution)

#-- Test 2: Add in MAC, it should not make a difference for Color mapping problem.
def test_2():
    print('Test 2: Map Coloring CSP with inferencing.----------------------------')
    mapColoringProblem = MapColoringProblem()
    print(mapColoringProblem)
    solution = backtracking_search(mapColoringProblem, mac=True)
    print(solution)

#-- Test 3: Use MRV, this should make a difference.
def test_3():
    print('Test 3: Map Coloring CSP with MRV.----------------------------')
    mapColoringProblem = MapColoringProblem()
    print(mapColoringProblem)
    solution = backtracking_search(mapColoringProblem, mrv=True)
    print(solution)

def test_4():
    print('Test 4: Map Coloring CSP with LCV.----------------------------')
    mapColoringProblem = MapColoringProblem()
    print(mapColoringProblem)
    solution = backtracking_search(mapColoringProblem, lcv=True)
    print(solution)

def test_5():
    print('Test 5: Map Coloring CSP with all heuristics and inferencing.----------------------------')
    mapColoringProblem = MapColoringProblem()
    print(mapColoringProblem)
    solution = backtracking_search(mapColoringProblem, mrv=True, lcv=True)
    print(solution)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
