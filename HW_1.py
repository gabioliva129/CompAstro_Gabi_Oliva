###  HW 1 -- found on Class Website
###  DUE 9/15/26
###      Write a program that calculates the time it takes for a ball to drop from a user specified
###      height to reach the ground. Use argparse. Also, let the user choose different values of gravity.
###      And any other features you think maybe interesting.


def fall_time(h, v_0, g):
    """
    the physics formulae are as follows:
        h = v_0 * t  +  1/2 a t^2
        --> t = -v_0 / g  +  sqrt(v_0^2/g^2 + 2h/g)

    inputs:
        h = height from which the ball is dropped (in meters above ground)
        v_0 = initial downward velocity of the ball, assumed 0 so ball is just dropped and not thrown
        g = gravitational constant, assumed 9.8 m/s^2

    outputs:
        t = time it takes for the ball to fall the given height

    assumptions:
        h is height above ground
        positive direction is towards the ground (v is downward velocity, g is positive)
    """
    t = -v_0 / g + ((v_0**2 / g**2) + 2*h/g)**0.5
    return t

if __name__ == "__main__":  # only uses argparse if this file is being directly run --> means I can import fall_time function in other files/directories

    import argparse  # I put the import under this section (if __name__ == "__main__") so that I can call fall_time somewhere else without having it import argparse there

    parser = argparse.ArgumentParser(prog='Ball Fall Time',  # name of the program
                        description="Use to calculate a ball's fall time from a user-given height. Initial velocity and the gravitational constant can also be changed. Solution comes from the formula:        h = v_0 * t  +  1/2 a t^2")

    parser.add_argument("height",  # in meters
                        type=float,
                        help="The height from which the ball falls from in meters.")

    parser.add_argument("--v_init",  # allows user to add an initial velocity to the ball if they want to solve for time in the case that the ball is not just dropped, but thrown with an initial downwards velocity
                        type=float,
                        default=0,  # m/s
                        help="The initial downward velocity of the ball in m/s. Default is 0 m/s.")

    parser.add_argument("--g",   # allows user to add a different gravitational constant to the environment if they want to solve for time in the case that the ball is on a different planet than Earth
                        type=float,
                        default=9.8,  # m/s^2
                        help="The gravitational constant. Default value is 9.8 m/s^2.")

    args = parser.parse_args()


    result = fall_time(args.height, args.v_init, args.g)
    print(f"The ball takes {result:.2f} seconds to reach the ground.")   # to 2 decimal places

