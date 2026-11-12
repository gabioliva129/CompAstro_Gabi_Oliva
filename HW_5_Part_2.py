# HW 5 Part 2
#
# Now to extend this calculation to the Sun we need to know the Sun’s electron density as a
# function of radius. A reasonably accurate fit is given as equation 4.2 in Neutrino Astrophysics
# by John Bachall. The formula is
#
# n_e(r) = 2.5 \times 10^{26} exp^{-\frac{r}{0.096 R_{sun}}}  cm^{-3}
#
# where R_{sun} is the solar radius, 696,340km. The formula is only good to 0.9R_{sun}, after which
# density drops quickly and one can assume there are no more scatterings for photons. So in some sense
# the Sun ends at 0.9R_{sun}. We can now calculate the time it takes for a photon to escape the Sun.
# Note that the mean free path changes by many orders of magnitude as the radius changes. So you can’t
# simply ask what is the probability of a photon scattering for some fixed distance, like 1cm. Instead,
# just like for radioactive decay, we can draw how long it took the photon to cross a distance from
# the Monte Carlo radiative transfer you did in part one. So perform say ~1000 runs of part A to
# determine the distribution of travel times to get through say ~10 mean free paths. Note since you
# will be using these results at different densities you want your answer to be in units of the mean
# free path (or the mean free travel time, l/c). You can either fit a function to the travel times or
# just keep the numerical values. Then perform a Monte Carlo simulation of the travel time for a photon
# through the Sun by drawing from a travel time at each density that the photon ends up at. Note that
# this is a fairly computationally intensive calculation. You will have to think about how long each
# part of the calculation takes, you will want to time them.


##########################################################################
## FUNCTIONS




##########################################################################


## IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

