# Day 1  -- Computational Astrophysics

"""
- uv add [package name].    ---> see pyproject.toml
- created a venv for Comp_Astro folder
- took notes on INTRO TO PYTHON from Course Website (in physical notebook)
- Exercise 4 (below)
"""







# EXERCISE 4:
#   write a function that given the height of the ball
#   determines the amount of time it takes to hit the ground

def time_to_ground(given_height, g=9.8):
    """
    inputs:
    - given_height = initial height of object in m
    - g = gravitational constant in m/s^2

    return:
    - time = time it takes object to fall in seconds
    """
    time = (2 * given_height / g)**0.5 # seconds
    return time


if __name__ == "__main__":
    print(time_to_ground(100))

    x = "Hello World"
    print(x.upper())


