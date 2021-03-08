#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:44:59 2021

@author: sunlu
"""

import numpy as np
import LinearProgramming as lp

lp_demo = lp.LinearProgramming("cmax", np.array([40,30]))
lp_demo.reset_inequality_constraint_a(np.array([[1,1],[2,1]]))
lp_demo.reset_inequality_constraint_b(np.array([[240],[320]]))
lp_demo.reset_lower_bound(np.array([[0],[0]]))
lp_demo.solve_gurobi()
lp_demo.display_result()
