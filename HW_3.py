###    HW3 –- Exercise 6.16: The Lagrange Point
###    DUE 10/1/26
#
# There is a magical point between the Earth and the Moon, called the L1 Lagrange point,
# at which a satellite will orbit the Earth in perfect synchrony with the Moon, staying always in between the two.
# This works because the inward pull of the Earth and the outward pull of the Moon combine to create exactly the
# needed centripetal force that keeps the satellite in its orbit. Here’s the setup:
#
# Assuming circular orbits, and assuming that the Earth is much more massive than either the Moon or the satellite,
# show that the distance r from the center of the Earth to the L1 point satisfies

# {GM\over r^2} - {Gm\over(R-r)^2} = \omega^2 r,
#
# where M and m are the Earth and Moon masses, G is Newton’s gravitational constant, and ω is the angular velocity of
# both the Moon and the satellite.
#
# The equation above is a fifth-order polynomial equation in r (also called a quintic equation).
# Such equations cannot be solved exactly in closed form, but it’s straightforward to solve them numerically.
# Write a program that uses either Newton’s method or the secant method to solve for the distance r from the Earth
# to the L1 point. Compute a solution accurate to at least four significant figures.
#
# The values G and the Earth’s mass can be found in the astropy.constants or scipy.constants sub-packages.
# The Moon’s mass is 7.348e22 kg and the Earth-Moon distance is 3.844e8 m. The value of ω is 2.662e-6 s-1.
# You will also need to choose a suitable starting value for r, or two starting values if you use the secant
# method.


###################################################################################################################

### NOTES
# GM/r^2 - Gm/(R-r)^2 = w^2 r
# --> we want to solve for r that is less than R
# --> rearrange the equation:
# f(r) = w^2 r^5  - 2Rw^2 r^4  +  w^2R^2 r^3  +  (Gm - GM) r^2  +  2GMR r  - GMR^2 = 0


### DEFINING FUNCTIONS

def func_of_r(r, a1, a2, a3, a4, a5, a6):
    return a1*r**5 + a2*r**4 + a3*r**3 + a4*r**2 + a5*r + a6


def deriv_func(r, a1, a2, a3, a4, a5):
    return 5*a1*r**4 + 4*a2*r**3 + 3*a3*r**2 + 2*a4*r + a5


def newton_meth(a1, a2, a3, a4, a5, a6, r_guess=3.0e8, accuracy=1e-4):
    r = r_guess
    error = 1
    iterations = 0  # gives info about how many iterations were necessary to get within accuracy level

    while error > accuracy:
        f = func_of_r(r, a1, a2, a3, a4, a5, a6)
        f_prime = deriv_func(r, a1, a2, a3, a4, a5)

        r_prime = r - f / f_prime

        error = np.abs((r_prime - r) / r_prime)
#        error = np.abs(r_prime - r)

        r = r_prime
        iterations += 1

    return r, iterations, error



###################################################################################################################


if __name__ == "__main__":
    ### IMPORTS
    from astropy import constants as const
    # from astropy import units as u
    import numpy as np
    import argparse
    from matplotlib import pyplot as plt


    ### SETTING UP ARGPARSE
    parser = argparse.ArgumentParser(prog='Finding L1 Point of a Satellite between Earth and Moon',  # name of the program
                                     description="Finds the minimum of the equation of motion equation      GM/r^2 - Gm/(R-r)^2 = r*omega^2    to find the Lagrange 1 Point for a Satellite orbiting between the Moon and the Earth. Found using Newton's Method")

    parser.add_argument("--display_plot",
                        type=bool,
                        default=False,
                        help="Type = Boolean. If True, a plot of the given equation of motion as a function of r will be displayed. Default is False (plot is not displayed).")

    parser.add_argument("--r_guess",
                        type=float,
                        default=3.0e8,
                        help="The initial guess for the Newton's Method calculations for the distance of the satellite from the Earth. Found from graph. Default value is 3.0e8 m.")

    parser.add_argument("--accuracy",
                        type=float,
                        default=1e-4,
                        help="The accuracy value for which the Newton's Method calculation will get the distance between the Earth and Satellite within before stopping. Default value is 0.0001 m.")

    parser.add_argument("--print_iterations",
                        type=bool,
                        default=False,
                        help="Type = Boolean. When True, this will print the number of iterations through Newton's Method were required to arrive at the answer for L1 within the given accuracy. Default is False (value is not printed).")

    parser.add_argument("--print_error",
                        type=bool,
                        default=False,
                        help="Type = Boolean. When True, this will print the error value on the calculation for the L1 distance. Default is False (value is not printed).")

    args = parser.parse_args()



    ### CONSTANTS
    G = const.G.value
    M_Earth = const.M_earth.value
    m_Moon = 7.348e22  # kg
    omega = 2.662e-6  #1/s
    R = 3.844e8  # m


    ### SOLVING
    a1 = omega**2
    a2 = -2 * R * omega**2
    a3 = omega**2 * R**2
    a4 = (G*m_Moon - G*M_Earth)
    a5 = 2 * G * M_Earth * R
    a6 = -G * M_Earth * R**2

    r_vals = np.arange(0, R, 100000)
    y_vals = func_of_r(r_vals, a1, a2, a3, a4, a5, a6)



    ### CALLING FUNCTION
    answer = newton_meth(a1, a2, a3, a4, a5, a6, args.r_guess, args.accuracy)
    r_answer = answer[0] / 1e8        # in scientific notation in units of 1e8 m
    print(f"The distance from the Earth to the L1 Point for a Satellite is {r_answer:.3f}e8 meters.")

    if args.print_iterations == True:
        print(f"Calculations took {answer[1]} iterations.")

    if args.print_error == True:
        print(f"Error = +/- {answer[2]} m.")



    ### PLOTTING
    if args.display_plot == True:
        plt.figure(figsize=(8,6))
        plt.plot(r_vals, y_vals)
        plt.axhline(y=0, color="hotpink", linestyle="--")
        # plt.axvline(x=r_answer*1e8, color="hotpink", linestyle="--")
        plt.ylabel(r"$f (r)$")
        plt.xlabel("Distance of Satellite from the Earth (m)")

        box_style = dict(boxstyle='round', facecolor='hotpink', alpha=0.35, edgecolor='black')
        text_string = (r'$f(r) = \frac{GM}{r^2} - \frac{Gm}{(R-r)^2} -\omega^2r$')
        plt.title(r"Minimizing Equations of Motion (Finding r where $f(r)=0$)")
        plt.text(2e8, -5e31, text_string, fontsize=16, bbox=box_style)

        plt.show()
