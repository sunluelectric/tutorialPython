# -*- coding: utf-8 -*-
"""
Class: LinearProgramming
"""

import numpy as np
import gurobipy as gp

class LinearProgramming():
    """
    LinProg defines and solves a LP problem.
    """
    def __init__(self, *args):
        """
        __init__ creates a LP problem.
        """
        try:
            problem_configuration = self._listtodict(list(args))
        except SyntaxError:
            print("Syntax error in the configuration of the LP problem.\n")
        if ("cmax" in problem_configuration.keys())\
            and ("cmin" not in problem_configuration.keys()):
            self.minimize_problem = False
            self.costfunction_matrix = -problem_configuration.get("cmax")
        elif ("cmin" in problem_configuration.keys())\
            and ("cmax" not in problem_configuration.keys()):
            self.minimize_problem = True
            self.costfunction_matrix = problem_configuration.get("cmin")
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
        self.canonical_flag = False
        # Variables used in the class
        self.canonical_max_kpi = None
        self.canonical_inequality_constraint_a = None
        self.canonical_inequality_constraint_b = None
        self.gurobi_lp_model = None
        self.gurobi_lp_variable = None
        self.optimum_x = None
        self.optimum_y = None
    def reset_costfunction_matrix(self, *args):
        """
        reset_costfunction_matrix resets the cost function matrix of the LP problem.
        """
        try:
            problem_configuration = self._listtodict(list(args))
        except SyntaxError:
            print("Syntax error in the configuration of the LP problem.\n")
        if ("cmax" in problem_configuration.keys())\
            and ("cmin" not in problem_configuration.keys()):
            self.minimize_problem = False
            self.costfunction_matrix = -problem_configuration.get("cmax")
        elif ("cmin" in problem_configuration.keys())\
            and ("cmax" not in problem_configuration.keys()):
            self.minimize_problem = True
            self.costfunction_matrix = problem_configuration.get("cmin")
        else:
            self.costfunction_matrix = None
            self.minimize_problem = None
        self.consistency_flag = False
        self.canonical_flag = False
    def reset_inequality_constraint_a(self, inequality_constraint_a):
        """
        reset_inequality_constraint_a resets the inequality constraint a
        """
        self.inequality_constraint_a = inequality_constraint_a
        self.consistency_flag = False
        self.canonical_flag = False
    def reset_inequality_constraint_b(self, inequality_constraint_b):
        """
        reset_inequality_constraint_b resets the inequality constraint b
        """
        self.inequality_constraint_b = inequality_constraint_b
        self.consistency_flag = False
        self.canonical_flag = False
    def reset_lower_bound(self, lower_bound):
        """
        reset_lower_bound resets the lower bound of the LP problem.
        """
        self.lower_bound = lower_bound
        self.consistency_flag = False
        self.canonical_flag = False
    def reset_upper_bound(self, upper_bound):
        """
        reset_upper_bound resets the upper bound of the LP problem.
        """
        self.upper_bound = upper_bound
        self.consistency_flag = False
        self.canonical_flag = False
    @classmethod
    def _listtodict(cls, input_lst):
        """
        _listtodict converts an input list to a dictionary.
        """
        output_op = {input_lst[i]: input_lst[i + 1] for i in range(0, len(input_lst), 2)}
        return output_op
    def _check_consistency(self):
        """
        Check input consistency
        """
        consistency_flag = True
        # Check cost function and inequality matrix size constraint consistency.
        if self.costfunction_matrix is not None:
            variable_length = len(self.costfunction_matrix)
            if (self.inequality_constraint_a is not None)\
                and (self.inequality_constraint_b is not None):
                inequality_constraint_length = len(self.inequality_constraint_b)
                if self.inequality_constraint_a.shape[1] == variable_length:
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
                      for the LP problem.\n")
                consistency_flag = False
        else:
            print("The cost function matrix is not defined for the LP problem.\n")
            consistency_flag = False
        # Check upper bound and lower bound consistency.
        if consistency_flag:
            if self.upper_bound is not None:
                if len(self.upper_bound) == variable_length:
                    pass
                else:
                    print("The number of variables is not consistent\
                          in the cost function and in the upper bound setup\
                              for the LP problem.\n")
            if self.lower_bound is not None:
                if len(self.lower_bound) == variable_length:
                    pass
                else:
                    print("The number of variables is not consistent\
                          in the cost function and in the lower bound setup\
                              for the LP problem.\n")
        # Set flag
        self.consistency_flag = consistency_flag
        self.canonical_flag = False
    def _form_canonical(self):
        """
        _form_canonical forms the LP problem into canonical form.
        """
        if self.consistency_flag:
            variable_length = len(self.costfunction_matrix)
            self.canonical_max_kpi = -self.costfunction_matrix
            self.canonical_inequality_constraint_a = self.inequality_constraint_a
            self.canonical_inequality_constraint_b = self.inequality_constraint_b
            if self.upper_bound is not None:
                self.canonical_inequality_constraint_a = np.concatenate(\
                    (self.canonical_inequality_constraint_a, \
                     np.identity(variable_length)), axis = 0)
                self.canonical_inequality_constraint_b = np.concatenate(\
                    (self.canonical_inequality_constraint_b, \
                     self.upper_bound), axis = 0)
            if self.lower_bound is not None:
                self.canonical_inequality_constraint_a = np.concatenate(\
                    (self.canonical_inequality_constraint_a, \
                     -np.identity(variable_length)), axis = 0)
                self.canonical_inequality_constraint_b = np.concatenate(\
                    (self.canonical_inequality_constraint_b, \
                     self.lower_bound), axis = 0)
            self.canonical_flag = True
        else:
            print("The LP problem has not passed consistency check yet.\n")
    def solve_gurobi(self):
        """
        solve_gurobi solves the LP problem using gurobipy.model()
        """
        self._check_consistency()
        self._form_canonical()
        if self.consistency_flag and self.canonical_flag:
            variable_length = len(self.costfunction_matrix)
            self.gurobi_lp_model = gp.Model()
            self.gurobi_lp_model.Params.LogToConsole = 0
            self.gurobi_lp_variable = self.gurobi_lp_model.addMVar(variable_length)
            self.gurobi_lp_model.setMObjective(None, self.canonical_max_kpi, 0.0, \
                                               None, None, self.gurobi_lp_variable, \
                                                   gp.GRB.MAXIMIZE)
            self.gurobi_lp_model.addConstr(self.canonical_inequality_constraint_a \
                                           @ self.gurobi_lp_variable <= \
                                               self.canonical_inequality_constraint_b.transpose()[0]) # pylint: disable=line-too-long
            self.gurobi_lp_model.update()
            self.gurobi_lp_model.optimize()
            self.optimum_x = self.gurobi_lp_variable.x
            self.optimum_y = self.gurobi_lp_model.objVal
        else:
            print("The LP problem has not passed consistency check\
                  or formed into a canonical form yet.\n")
    def display_result(self):
        """
        display_result displays the result of the LP problem
        """
        print("The optimum x variables are: \n")
        print(self.optimum_x)
        print("\n")
        if self.minimize_problem:
            print("The cost function value is: \n")
            print(-self.optimum_y)
        elif not self.minimize_problem:
            print("The likelihood function value is: \n")
            print(self.optimum_y)
        print("\n")
