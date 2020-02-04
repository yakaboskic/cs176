from TemporalCSP import TemporalCSP
from backtracking_search import backtracking_search

#-- Test 1: Only Backtracking in Map Problem, No heuristics or inferencing.
def test_1():
    print('Test 1: Temporal CSP with no heuristic or inferencing.----------------------------')
    tcsp = TemporalCSP()
    #print(tcsp)
    solution = backtracking_search(tcsp)
    print(solution)

def test_2():
    print('Test 2: Temporal CSP with inferencing.----------------------------')
    tcsp = TemporalCSP()
    #print(tcsp)
    solution = backtracking_search(tcsp, mac=True, mrv=False, lcv=False)
    print(solution)

def test_3():
    print('Test 3: Temporal CSP with MRV.----------------------------')
    tcsp = TemporalCSP()
    #print(tcsp)
    solution = backtracking_search(tcsp, mac=False, mrv=True, lcv=False)
    print(solution)

def test_4():
    print('Test 4: Temporal CSP with LCV.----------------------------')
    tcsp = TemporalCSP()
    #print(tcsp)
    solution = backtracking_search(tcsp, mac=False, mrv=False, lcv=True)
    print(solution)

if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
