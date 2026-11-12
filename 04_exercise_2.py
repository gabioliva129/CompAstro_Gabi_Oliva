# 9/15/26
# Day 5 Lecture

# Lecture Notes 4 from Website CONTINUED
# NUMERICAL INTEGRATION


# Exercise 5.2

import gaussxw as g  # file from course notes, see file in current directory for explanation of functions
import numpy as np

def func(x):   # like function from 4_exercises.py
    y = x**4 -2*x +1
    return y

N = 100
a = 0
b = 2

x,w = g.gaussxw(N,a,b)
answer =  np.sum(func(x) * w)

print(answer)