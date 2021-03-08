#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:44:59 2021

@author: sunlu
"""

import numpy as np
import LinearProgramming as lp

lp_demo = lp.LinearProgramming("cmax", np.array([45,80]))
lp_demo.reset_inequality_constraint_a(np.array([[5,20],[10,15]]))
lp_demo.reset_inequality_constraint_b(np.array([[400],[450]]))
lp_demo.reset_lower_bound(np.array([[0],[0]]))
lp_demo.solve_gurobi()
lp_demo.display_result()
