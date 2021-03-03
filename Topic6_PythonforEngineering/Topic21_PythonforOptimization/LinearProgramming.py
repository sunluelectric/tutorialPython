# -*- coding: utf-8 -*-
"""
Class: LinearProgramming
"""

class LinProg():
    """
    LinProg defines and solves a linear programming problem.
    """
    def __init__(self, *args):
        """
        __init__ creates a linear programming problem.
        """
        try:
            problem_configuration = self._listtodict(list(args))
        except SyntaxError:
            print("Syntax error in the configuration of the linear programming problem.\n")
        if "c" in problem_configuration.keys():
            self.costfunction_matrix = problem_configuration.get("c")
        else:
            self.costfunction_matrix = None
        if "ineq_a" in problem_configuration.keys():
            self.inequality_constraint_a = problem_configuration.get("ineq_a")
        else:
            self.inequality_constraint_a = None
        if "ineq_b" in problem_configuration.keys():
            self.inequality_constraint_b = problem_configuration.get("ineq_b")
        else:
            self.inequality_constraint_b = None
        if "lb" in problem_configuration.keys():
            self.lower_bound = problem_configuration.get("lb")
        else:
            self.lower_bound = None
        if "ub" in problem_configuration.keys():
            self.upper_bound = problem_configuration.get("ub")
        else:
            self.upper_bound = None
        self.consistency_flag = False
    def reset_costfunction_matrix(self, costfunction_matrix):
        """
        reset_costfunction_matrix resets the cost function matrix of the linear programming problem.
        """
        self.costfunction_matrix = costfunction_matrix
        self.consistency_flag = False
    def reset_inequality_constraint_a(self, inequality_constraint_a):
        """
        reset_inequality_constraint_a resets the inequality constraint a
        """
        self.inequality_constraint_a = inequality_constraint_a
        self.consistency_flag = False
    def reset_inequality_constraint_b(self, inequality_constraint_b):
        """
        reset_inequality_constraint_b resets the inequality constraint b
        """
        self.inequality_constraint_b = inequality_constraint_b
        self.consistency_flag = False
    def reset_lower_bound(self, lower_bound):
        """
        reset_lower_bound resets the lower bound of the linear programming problem.
        """
        self.lower_bound = lower_bound
        self.consistency_flag = False
    def reset_upper_bound(self, upper_bound):
        """
        reset_upper_bound resets the upper bound of the linear programming problem.
        """
        self.upper_bound = upper_bound
        self.consistency_flag = False
    @classmethod
    def _listtodict(cls, input_lst):
        """
        _listtodict converts a input list to a dictionary.
        """
        output_op = {input_lst[i]: input_lst[i + 1] for i in range(0, len(input_lst), 2)}
        return output_op
    def _check_consistency(self):
        """
        Check input consistency
        """
        consistency_flag = True
        # Check cost function and inequality constraint consistency.
        if self.costfunction_matrix is not None:
            variable_length = len(self.costfunction_matrix)
            if (self.inequality_constraint_a is not None)\
                and (self.inequality_constraint_b is not None):
                inequality_constraint_length = len(self.inequality_constraint_b)
                if self.inequality_constraint_a.shape[0] == variable_length:
                    pass
                else:
                    print("The number of variables is not consistent\
                          in the cost function and in the inequality constraint.\n")
                    consistency_flag = False
                if self.inequality_constraint_a.shape[0] == inequality_constraint_length:
                    pass
                else:
                    print("The number of inequality constraint number is not consistent\
                          in ineq_a and ineq_b.\n")
                    consistency_flag = False
            else:
                print("The inequality constraint is not defined\
                      for the linear programming problem.\n")
                consistency_flag = False
        else:
            print("The cost function matrix is not defined for the linear programming problem.\n")
            consistency_flag = False
        # Check upper bound and lower bound consistency.
        if consistency_flag:
            if self.upper_bound is not None:
                if len(self.upper_bound) == variable_length:
                    pass
                else:
                    print("The number of variables is not consistent\
                          in the cost function and in the upper bound setup\
                              for the linear programming problem.\n")
            if self.lower_bound is not None:
                if len(self.lower_bound) == variable_length:
                    pass
                else:
                    print("The number of variables is not consistent\
                          in the cost function and in the lower bound setup\
                              for the linear programming problem.\n")
        # Set flag
        self.consistency_flag = consistency_flag
    