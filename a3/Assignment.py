# CSP Assignment
# Original code by Håkon Måløy
# Updated by Xavier Sánchez Díaz

import copy
from itertools import product as prod


class CSP:
    backtrack_called = 0
    backtrack_failed = 0
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains is a dictionary of domains (lists)
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

    def add_variable(self, name: str, domain: list):
        """Add a new variable to the CSP.

        Parameters
        ----------
        name : str
            The name of the variable to add
        domain : list
            A list of the legal values for the variable
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a: list, b: list) -> list[tuple]:
        """Get a list of all possible pairs (as tuples) of the values in
        lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.

        Parameters
        ----------
        a : list
            First list of values
        b : list
            Second list of values

        Returns
        -------
        list[tuple]
            List of tuples in the form (a, b)
        """
        return prod(a, b)

    def get_all_arcs(self) -> list[tuple]:
        """Get a list of all arcs/constraints that have been defined in
        the CSP.

        Returns
        -------
        list[tuple]
            A list of tuples in the form (i, j), which represent a
            constraint between variable `i` and `j`
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var: str) -> list[tuple]:
        """Get a list of all arcs/constraints going to/from variable 'var'.

        Parameters
        ----------
        var : str
            Name of the variable

        Returns
        -------
        list[tuple]
            A list of all arcs/constraints in which `var` is involved
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i: str, j: str,
                               filter_function: callable):
        """Add a new constraint between variables 'i' and 'j'. Legal
        values are specified by supplying a function 'filter_function',
        that should return True for legal value pairs, and False for
        illegal value pairs.

        NB! This method only adds the constraint one way, from i -> j.
        You must ensure to call the function the other way around, in
        order to add the constraint the from j -> i, as all constraints
        are supposed to be two-way connections!

        Parameters
        ----------
        i : str
            Name of the first variable
        j : str
            Name of the second variable
        filter_function : callable
            A callable (function name) that needs to return a boolean.
            This will filter value pairs which pass the condition and
            keep away those that don't pass your filter.
        """
        if j not in self.constraints[i]:
            # First, get a list of all possible pairs of values
            # between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(
                self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = list(filter(lambda
                                             value_pair:
                                             filter_function(*value_pair),
                                             self.constraints[i][j]))

    def add_all_different_constraint(self, var_list: list):
        """Add an Alldiff constraint between all of the variables in the
        list provided.

        Parameters
        ----------
        var_list : list
            A list of variable names
        """
        for (i, j) in self.get_all_possible_pairs(var_list, var_list):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        

        if all(len(e) == 1 for e in assignment.values()): #Is one value for each assignment, CSP is complete
            return assignment
        var = self.select_unassigned_variable(assignment) #Get a variable whose value is yet to be decided

        for value in assignment[var]:
            deep_copy_assignment = copy.deepcopy(assignment) #Do not overwrite original in case needs to go back
            deep_copy_assignment[var] = [value] #Try a value for the variable
            inference = self.inference(deep_copy_assignment, self.get_all_arcs()) #Find potential assignments for the others

            if inference: #If potential assignments were found
                result = self.backtrack(deep_copy_assignment) #Backtrack to find more
                if result != None:
                    #Calling backtrack, count it
                    self.backtrack_called += 1
                    return result

        #Backtrack failed, count it
        self.backtrack_failed += 1    
        return None

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        for key, value in assignment.items(): #Currently only returns the first var with more than 1 values, could be better heuristic here
            if len(value) > 1:
                return key
        return None

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        while queue: #While arcs to be checked
            (xi, xj) = queue.pop()
            if self.revise(assignment, xi, xj): #If have to revise the value for the given arc
                if len(assignment[xi]) == 0: #One variable has empty domain, CSP cannot be solved
                    return False
                
                #Getting all the relevant neighbouring arcs and adding them to the queue to be checked 
                neighboring_arcs = self.get_all_neighboring_arcs(xi)
                neighboring_arcs.remove((xj, xi)) 
                for xk in neighboring_arcs:
                    queue.append(xk)
        return True

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """

        revised = False
        for x in assignment[i]: #For all potential values for variable i
            if not any((x, y) in self.constraints[i][j] for y in assignment[j]): #If there is no potential values for variable j such that a combination of their values satisfy the constraint 
                assignment[i].remove(x) #Remove value x from potential values for variable i to get towards a state where one value is left for i
                revised = True
        return revised #Return whether potential values for i has been reduced or not


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
             'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
    colors = ['red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp


def create_sudoku_csp(filename: str) -> CSP:
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.

    Parameters
    ----------
    filename : str
        Filename of the Sudoku board to solve

    Returns
    -------
    CSP
        A CSP instance
    """
    csp = CSP()
    board = list(map(lambda x: x.strip(), open(filename, 'r')))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), list(map(str,
                                                                range(1, 10))))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col)
                                          for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col)
                                         for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp


def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print(solution['%d-%d' % (row, col)][0], end=" "),
            if col == 2 or col == 5:
                print('|', end=" "),
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')


"""~~~PRINTING RESULTS HERE~~~"""

print("Printing for map csp too")
map_csp = create_map_coloring_csp()
print(map_csp.backtracking_search())
print("Backtrack called " + str(map_csp.backtrack_called) + " times")
print("Backtrack failed " + str(map_csp.backtrack_failed) + " times")
print()

print("Easy")
sudoku_csp = create_sudoku_csp("a3/easy.txt")
print_sudoku_solution(sudoku_csp.backtracking_search())
print("Backtrack called " + str(sudoku_csp.backtrack_called) + " times")
print("Backtrack failed " + str(sudoku_csp.backtrack_failed) + " times")
print()

print("Medium")
sudoku_csp_medium = create_sudoku_csp("a3/medium.txt")
print_sudoku_solution(sudoku_csp_medium.backtracking_search())
print("Backtrack called " + str(sudoku_csp_medium.backtrack_called) + " times")
print("Backtrack failed " + str(sudoku_csp_medium.backtrack_failed) + " times")
print()

print("Hard")
sudoku_csp_hard = create_sudoku_csp("a3/hard.txt")
print_sudoku_solution(sudoku_csp_hard.backtracking_search())
print("Backtrack called " + str(sudoku_csp_hard.backtrack_called) + " times")
print("Backtrack failed " + str(sudoku_csp_hard.backtrack_failed) + " times")
print()

print("Very hard")
sudoku_csp_veryhard = create_sudoku_csp("a3/veryhard.txt")
print_sudoku_solution(sudoku_csp_veryhard.backtracking_search())
print("Backtrack called " + str(sudoku_csp_veryhard.backtrack_called) + " times")
print("Backtrack failed " + str(sudoku_csp_veryhard.backtrack_failed) + " times")