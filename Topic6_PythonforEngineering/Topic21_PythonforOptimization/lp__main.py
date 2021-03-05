#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:44:59 2021

@author: sunlu
"""

import numpy as np
import LinearProgramming as lp

demo_lp = lp.LinearProgramming("c", np.array([-45,-80]))
demo_lp.reset_inequality_constraint_a(np.array([[5,20],[10,15]]))
demo_lp.reset_inequality_constraint_b(np.array([[400],[450]]))
demo_lp.reset_lower_bound(np.array([[0],[0]]))
demo_lp.solve_gurobi()
demo_lp.display_result()
