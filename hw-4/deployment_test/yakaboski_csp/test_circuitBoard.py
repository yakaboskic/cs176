from CircuitBoardProblem import Circuit, CircuitBoard, CircuitBoardProblem
from backtracking_search import backtracking_search

#-- Circuits and board that will be used in our tests
circuit_a = Circuit(3,2)
circuit_b = Circuit(5,2, letter_rep='b')
circuit_c = Circuit(2,3, letter_rep='c')
circuit_e = Circuit(7,1, letter_rep='e')
cb = CircuitBoard(10, 3)

#-- Test of printing of circuit board. Should match assignment page.
def test_1():
    print('Test of Circuit Board Layout Printing. ----------------')
    cb = CircuitBoard(10, 3, chips={circuit_a: (0,0),
                                    circuit_b: (3,0),
                                    circuit_c: (8,0),
                                    circuit_e: (0,2)})
    print(cb)


#-- Run Circuit Board CSP with no added heuristics or inferencing.
def test_2():
    print('Test 2: Circuit Board CSP with no heuristic or inferencing.----------------------------')
    csp = CircuitBoardProblem(cb, [circuit_a, circuit_b, circuit_c, circuit_e])

    #-- If you want to print the problem just uncomment below. There are lots of constraints tho so beware of the output.
    #print(csp)

    solution = backtracking_search(csp, mrv=False, lcv=False, mac=False)
    print(solution)

#-- Run Circuit Board CSP with inferencing (MAC-3).
def test_3():
    print('Test 3: Circuit Board CSP with MAC-3 Inferencing.--------------------------------------')
    csp = CircuitBoardProblem(cb, [circuit_a, circuit_b, circuit_c, circuit_e])

    #-- If you want to print the problem just uncomment below. There are lots of constraints tho so beware of the output.
    #print(csp)

    solution = backtracking_search(csp, mrv=False, lcv=False, mac=True)
    print(solution)


#-- Run Circuit Board CSP with MRV heuristics.
def test_4():
    print('Test 4: Circuit Board CSP with MRV heuristic.------------------------------------------')
    csp = CircuitBoardProblem(cb, [circuit_a, circuit_b, circuit_c, circuit_e])

    #-- If you want to print the problem just uncomment below. There are lots of constraints tho so beware of the output.
    #print(csp)

    solution = backtracking_search(csp, mrv=True, lcv=False, mac=False)
    print(solution)


#-- Run Circuit Board CSP with LVC heuristic.
def test_5():
    print('Test 5: Circuit Board CSP with LVC heuristic.------------------------------------------')
    csp = CircuitBoardProblem(cb, [circuit_a, circuit_b, circuit_c, circuit_e])

    #-- If you want to print the problem just uncomment below. There are lots of constraints tho so beware of the output.
    #print(csp)

    solution = backtracking_search(csp, mrv=False, lcv=True, mac=False)
    print(solution)


#-- Run Circuit Board CSP with all heuristics and inferencing together.
def test_6():
    print('Test 6: Circuit Board CSP with all heuristics and inferencing togther. ----------------')
    csp = CircuitBoardProblem(cb, [circuit_a, circuit_b, circuit_c, circuit_e])

    #-- If you want to print the problem just uncomment below. There are lots of constraints tho so beware of the output.
    #print(csp)

    solution = backtracking_search(csp, mrv=True, lcv=True, mac=True)
    print(solution)

#-- Bigger Board with more circuits. 
circuit_f = Circuit(3,2, letter_rep='f')
circuit_g = Circuit(5,2, letter_rep='g')
circuit_h = Circuit(2,3, letter_rep='h')
circuit_i = Circuit(7,1, letter_rep='i')


#-- Let's extend the board by a factor of 2 along the x-axis.
def test_7():
    big_board = CircuitBoard(20, 3)
    print('Test 7: Big Circuit Board CSP with no heuristic or inferencing.----------------------------')
    csp = CircuitBoardProblem(big_board, [circuit_a, circuit_b, circuit_c, circuit_e,
                                          circuit_f, circuit_g, circuit_h, circuit_i])

    #-- If you want to print the problem just uncomment below. There are lots of constraints tho so beware of the output.
    #print(csp)

    solution = backtracking_search(csp, mrv=False, lcv=False, mac=False)
    print(solution)
    
def test_8():
    big_board = CircuitBoard(20, 3)
    print('Test 8: Big Circuit Board CSP with all heuristic or inferencing.----------------------------')
    csp = CircuitBoardProblem(big_board, [circuit_a, circuit_b, circuit_c, circuit_e,
                                          circuit_f, circuit_g, circuit_h, circuit_i])

    #-- If you want to print the problem just uncomment below. There are lots of constraints tho so beware of the output.
    #print(csp)

    solution = backtracking_search(csp, mrv=True, lcv=True, mac=True)
    print(solution)

#-- Let's extend the board by a factor of 2 along the y-axis.
def test_9():
    big_board = CircuitBoard(10, 6)
    print('Test 9: Big Circuit Board CSP with no heuristic or inferencing.----------------------------')
    csp = CircuitBoardProblem(big_board, [circuit_a, circuit_b, circuit_c, circuit_e,
                                          circuit_f, circuit_g, circuit_h, circuit_i])

    #-- If you want to print the problem just uncomment below. There are lots of constraints tho so beware of the output.
    #print(csp)

    solution = backtracking_search(csp, mrv=False, lcv=False, mac=False)
    print(solution)
    
def test_10():
    big_board = CircuitBoard(10, 6)
    print('Test 10: Big Circuit Board CSP with all heuristics and inferencing.----------------------------')
    csp = CircuitBoardProblem(big_board, [circuit_a, circuit_b, circuit_c, circuit_e,
                                          circuit_f, circuit_g, circuit_h, circuit_i])

    #-- If you want to print the problem just uncomment below. There are lots of constraints tho so beware of the output.
    #print(csp)

    solution = backtracking_search(csp, mrv=True, lcv=True, mac=True)
    print(solution)
if __name__ == '__main__':
    #test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    test_7()
    test_8()
    test_9()
    test_10()
