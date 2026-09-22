# Lecture 5 Notes -- Differentiation (Derivatives)
# 9/17/26

# Exercise 5.15

import numpy as np
import matplotlib.pyplot as plt


def tanh_func(x):
        result = 1/2 * np.tanh(2*x)
        return result

def deriv_func(func, x, h=1e-5):
    df_dx = (func(x + h/2) - func(x - h/2)) / h
    return df_dx

def sec2(x):
    answer = 1 / (np.cosh(2 * x))** 2
    return answer



if __name__ == "__main__":
    interval = np.linspace(-2, 2, 500)
    plt.plot(interval, deriv_func(tanh_func, interval), label="manual", color="blue")
    plt.plot(interval, sec2(interval), label="solved", color="red")
    plt.legend()
    plt.show()
