###  HW 2 -- Exercise 5.3: Integration
###  DUE 9/22/26
###     Consider the integral
###     E(x) = \int^x_0 e^{-t^2} dt
###
###     a) Write a program to calculate E(x) for values of x from 0 to 3 in steps of 0.1. Choose for
###     yourself what method you will use for performing the integral and a suitable number of slices.
###
###     b) When you are convinced your program is working, extend it further to make a graph of E(x) as a
###     function of x.
###
###     Note that there is no known way to perform this particular integral analytically,
###     so numerical approaches are the only way forward.




################### ---     PART A   --- ###################


def func_in_integral(t):
    return np.e**(-t**2)

def intervals(start = 0, stop = 3, step_size = 0.1):
    return np.arange(start, stop + step_size, step_size)   # this is the x for the summation, not t

if __name__ == "__main__":
    # imports
    import numpy as np
    from scipy.integrate import quad
    import argparse
    from matplotlib import pyplot as plt

    # setting up argparse arguments
    parser = argparse.ArgumentParser(prog='Solving E(x) Integral',  # name of the program
                        description="Use to calculate the value of the integral     E(x) = int^x_0 e^{-t^2} dt      along a user-inputted range of x-values.")

    parser.add_argument("--start",
                        type = float,
                        default = 0,
                        help = "The start value which represents the lower-end of the range of x-values for which E(x) is evaluated on. Default value is 0.")

    parser.add_argument("--stop",
                        type = float,
                        default = 3,
                        help = "The stop value which represents the higher-end of the range of x-values for which E(x) is evaluated on. Default value is 3.")

    parser.add_argument("--step_size",
                        type = float,
                        default = 0.1,
                        help = "The step size which the main function will be evaluated over when integrating in between the Stop and Start values. Default value is 0.1.")

    parser.add_argument("--print_E_of_x_values",
                        type=bool,
                        default=True,
                        help="Type = Boolean. When True, this will print the values for E(x) from the given (or default) range and step size. Default is True (values are printed).")

    parser.add_argument("--print_E_error_values",
                        type=bool,
                        default=False,
                        help="Type = Boolean. If True, this will print the value of the error for evaluations of E at each x determined by the given (or default) range and step size. Default is False (values are not printed).")

    parser.add_argument("--display_plot",
                        type=bool,
                        default=True,
                        help="Type = Boolean. If True, a plot of the equation, E, as a function of x will be displayed. Default is True (plot is displayed).")

    args = parser.parse_args()



    # calling the functions and solving/saving in arrays
    E_of_x = []
    E_error = []

    for x in intervals(args.start, args.stop, args.step_size):
        value, error = quad(func_in_integral, 0, x)
            # scipy.integrate.quad automatically calculates the error in each integration evaluation.
            # Using the Quadrature method of integration. Though it is a tad involved/complex for the shape of the resulting graph and the areas it is finding.
        E_of_x.append(value)
        E_error.append(error)

    if args.print_E_of_x_values == True:
        print(f"The values of E(x) from x = {args.start} to x = {args.stop} with a step size of {args.step_size} are: ")
        for value in E_of_x:
            print("    ", value)

    if args.print_E_error_values == True:
        print(f"The error values of E(x) from x = {args.start} to x = {args.stop} with a step size of {args.step_size} are: ")
        for value2 in E_error:
            print("    ", value2)



    #################   PART B   #################

    if args.display_plot == True:
        plt.figure(figsize=(10, 7))
        plt.plot(intervals(args.start, args.stop, args.step_size), E_of_x, color="hotpink")
        plt.errorbar(intervals(args.start, args.stop, args.step_size), E_of_x, yerr=E_error, fmt='o', ecolor='navy', elinewidth=1, capsize=12, capthick=1.5, color='mediumvioletred')

        plt.title("Value of E(x)", fontsize=18)
        plt.xlabel("x", fontsize=14)
        plt.ylabel("Value of Integral", fontsize=14)

        box_style = dict(boxstyle='round', facecolor='thistle', alpha=0.5, edgecolor='black')
        text_string = r'$E(x) = \int^x_0 e^{-t^2} dt$'
        plt.text(args.start + 1, 0.1, text_string, fontsize=14, bbox=box_style)

        plt.show()
