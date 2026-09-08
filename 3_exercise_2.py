# exercise on quadratic equation

"""
Write a program that takes as
input 3 numbers; a, b and c and
prints out two solutions to the
quadratic equation.

Use your program to compute the
solution to 0.001x2 + 1000x +
0.001 = 0
"""


def plus(a,b,c):
    x = (-b + (b**2 - 4*a*c)**(1/2))/(2*a)

def minus(a,b,c):
    x = (-b + (b**2 - 4*a*c)**(1/2))/(2*a)

print(minus(0.001, 1000, 0.001))
print(plus(0.001, 1000, 0.001))
