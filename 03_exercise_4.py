# Exercise 4 -- Quantum Harmonic Oscillator:

import numpy as np

"""write a program to solve the
average energy in a quantum
harmonic oscillator which has
energy levels En = hf(n+1/2). 


hf=1, β=0.01

let us
evaluate this formula using a
thousand terms, a million
terms and a billion terms"""

hf = 1
beta = 1

def energy(n):
    En = hf * (n + 1/2)
    return En




n = 10

Z = []

E_avg = []
for i in range(n):
    Zn += np.e**(-beta*energy(i))
    Z = Z + Zn
    E += energy(n)*np.e**(-beta*energy(i))/Z
    print(E)

