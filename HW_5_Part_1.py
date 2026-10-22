###  HW 5 Part 1  -- Monte Carlo Radiative Transfer

# One of the most common uses of Monte Carlo calculations in astrophysics is for radiative transfer.
# The simplest example of this is the motion of radiation in a star. The cores of stars are hot and dense,
# such that all electrons are ionized and the cross section for most photons to interact with an electron
# is just the frequency independent Thompson cross-section.

# \sigma_T = \frac{8\pi}{3} \big(\frac{e^2}{4\pi \epsilon_0 m_e c^2}\big)^2  = 6.652 \times10^{-25} cm^2

# Another import quantity to consider in scattering theory is the mean free path of a particle.

# l = 1/(n \times\sigma)

# If n_e = 10^{20} cm^{-3} the mean free path would be 150m.

# Start by just considering a slab of constant electron density with this value and a width of 1km.
# Perform a Monte Carlo simulation of a photon through this slab. Note that for low energy photons
# (E = hf << m_e c^2) the photon scattering is isotropic, equally likely in any direction. However,
# since you are only trying to follow the photons progress through the slab, you only need to
# consider the angle the scattered photon makes with the direction through the slab.
# Also note that your photon is almost as likely to be reflected back to the beginning
# as make it through the slab, so make sure you account for this possibility. Make an animation of your
# photons path. One example of how to make an animation can be found here.



"""On HWs include:

- docstrings in functions
-
"""