###    HW3 – Exercise 6.16: The Lagrange Point
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
# The values G and the Earth’s mass can be found in the astropy.constants or scipy.constants sub-packages. The Moon’s mass is 7.348e22 kg and the Eart-Moon distance is 3.844e8 m. The value of ω is 2.662e-6 s-1. You will also need to choose a suitable starting value for r, or two starting values if you use the secant method.



m_Sun = 2.0e30  # kg
m_Moon = 7.348e22  # kg
omega = 2.662e-6  #1/s



