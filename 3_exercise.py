# checking machine precision of my computer
x = 1.0
eps = 1.0

while not x+eps == x:
    eps = 0.5*eps

print (2*eps)



b = 0.1
print(type(b))
print("{:30.20}".format(b))
import sys
sys.float_info

import numpy as np

print("")
x=1
y=x+10**(-14)*2**(1/2)
print(1e14*(y-x))
print(np.sqrt(2))
