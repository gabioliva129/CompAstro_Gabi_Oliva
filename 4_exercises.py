import numpy as np

def func(x):
    y = x**4 -2*x +1
    return y

def integral(y, a=0, b=2, slices=10):
    deltax = (b-a)/slices 
    total = 0.5*y(a)  + 0.5*y(b)

    for i in range(1, slices):
        total += y(a + i * deltax)

    int1 = deltax * total    
    return int1

p = [1,2,3]
x = np.sum(p) 



print("here, ", x)
print(integral(func, slices=1000))






def simpsons_integral(y, a=0, b=2, half_slices=500):
    deltax = (b-a)/(2*half_slices) 
    total = y(a)+ y(b)

    for i in range(1, half_slices):
        total += 4 * y(a + (2*i-1)*deltax)
    
    for i in range(1, half_slices - 1):
        total += 2 * y(a + 2*i*deltax)

    int2 = 1/3 * deltax * total    
    return int2

print(simpsons_integral(func, half_slices=1000))






