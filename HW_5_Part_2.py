# HW 5 Part 2
# DUE 11/19/26

# Now to extend this calculation to the Sun we need to know the Sun’s electron density as a
# function of radius. A reasonably accurate fit is given as equation 4.2 in Neutrino Astrophysics
# by John Bachall. The formula is n_e(r) = 2.5 \times 10^{26} exp^{-\frac{r}{0.096 R_{sun}}}  cm^{-3}
# where R_{sun} is the solar radius, 696,340km. The formula is only good to 0.9R_{sun}, after which
# density drops quickly and one can assume there are no more scatterings for photons. So in some sense
# the Sun ends at 0.9R_{sun}.
# We can now calculate the time it takes for a photon to escape the Sun. Note that the mean free path
# changes by many orders of magnitude as the radius changes. So you can’t
# simply ask what is the probability of a photon scattering for some fixed distance, like 1cm. Instead,
# just like for radioactive decay, we can draw how long it took the photon to cross a distance from
# the Monte Carlo radiative transfer you did in part one.
#
# ------ PART A: -------
# So perform say ~1000 runs of part A to determine the distribution of travel times to get through say
# ~10 mean free paths. Note since you will be using these results at different densities you want your
# answer to be in units of the mean free path (or the mean free travel time, l/c). You can either fit
# a function to the travel times or just keep the numerical values.
#
# ------ PART B: -------
# Then perform a Monte Carlo simulation of the travel time for a photon
# through the Sun by drawing from a travel time at each density that the photon ends up at.
# Note that this is a fairly computationally intensive calculation. You will have to think about
# how long each part of the calculation takes, you will want to time them.
#########################################################################################
#########################################################################################

## FUNCTIONS!!

def simulate_slab(slab_width=10.0):
    """ Simulates photon traveling through a slab.
    Returns the dimensionless travel
    time and exit direction.

    INPUTS:
        slab_width  --  width of sample slab in units of mean free path
    OUTPUTS:
        updates distances/speeds in x,y,z through random walk of
        particle while in the slab"""

    x, y, z = 0.0, 0.0, 0.0     # initial photon position
    vx, vy, vz = 1.0, 0.0, 0.0     # initial photon direction
    total_distance = 0.0

    while True:
        distance = -np.log(rng.random())   # random distance to the next scattering event

        # distance to the slab boundary
        if vx > 0:
            boundary_distance = (slab_width - x) / vx
        elif vx < 0:
            boundary_distance = -x / vx
        else:
            boundary_distance = np.inf

        # case where photon reaches a boundary before scattering
        if boundary_distance <= distance:
            total_distance += boundary_distance
            if vx > 0:
                return total_distance, "transmitted"
            else:
                return total_distance, "reflected"

        # photon continues to scatter --> update position
        x += distance * vx
        y += distance * vy
        z += distance * vz

        total_distance += distance

        # random isotropic scattering in 3D
        mu = 2.0 * rng.random() - 1.0
        phi = 2.0 * np.pi * rng.random()

        # update direction
        vx = mu
        vy = np.sqrt(1.0 - mu**2) * np.cos(phi)
        vz = np.sqrt(1.0 - mu**2) * np.sin(phi)


def solar_electron_dens(r):
    """as photon travels outward --> electron density decreases --> mean free path increases
       electron density as a function of radial position.
    INPUTS:
        r -- distance of particle from center of Sun
    OUTPUTS:
        density in electrons/m^3.
    """
    return n_init * np.exp(-r / (0.096 * R_sun))


def mean_free_path(r):
    return 1.0 / (solar_electron_dens(r) * sigma_T)


def diffusion(r):
    """diffusion in a star is:
        D = 1/3 * c * mean_free_path
    INPUTS:
        r -- photon radius from Sun center
    OUTPUTS:
        D -- diffusion coefficient """
    return speed_c * mean_free_path(r) / 3.0


def simulate_solar_photon():
    """ Simulates a photon traveling from center of the Sun
        to 0.9 Solar Radii.
     OUTPUTS:
        total escape time in seconds
        number of simulation steps"""

    x, y, z = 0.0, 0.0, 0.0  # photon's initial position at center
    total_time = 0.0 # initialing time

    for step in range(max_steps):
        r = np.sqrt(x**2 + y**2 + z**2)  # photon's current radial position

        if r >= R_sun_effective:    # stop stepping when photon reaches Sun's boundary
            return total_time, step

        mfp = mean_free_path(r)
        mean_free_time = mfp / speed_c

        # **randomly select dimensionless travel time from above code**
        random_time = rng.choice(travel_times)
        actual_time = random_time * mean_free_time  # convert dimensionless time to actual travel time

        D = diffusion(r)  # calculate local diffusion coefficient

        K = (0.0025 * scale_height / np.sqrt(6.0 * D * actual_time))  # expect a step to be 0.25% of the scale height over the diffusion step
        # print("K = ", K)
        actual_time *= K**2

        # estimating displacement using diffusion--> RMS displacement = sqrt(6 * D * actual_time)
        displacement = np.sqrt(6.0 * D * actual_time)

        # Generate random direction in 3D
        mu = 2.0 * rng.random() - 1.0
        phi = 2.0 * np.pi * rng.random()

        dx = displacement * mu
        dy = displacement * np.sqrt(1.0 - mu ** 2) * np.cos(phi)
        dz = displacement * np.sqrt(1.0 - mu ** 2) * np.sin(phi)

        # update photon's position after this step
        x += dx
        y += dy
        z += dz

        total_time += actual_time  # update travel time

        if step % 100000 == 0:
            print(
                f"Step: {step} | "
                f"Radius: {r / R_sun:.5f} R_sun | "
                f"Escape progress: {r / R_sun_effective * 100:.5f}%")

    raise RuntimeError(
        "Maximum number of steps reached. "
        "Increase max_steps."
    )


#########################################################################################

if __name__ == "__main__":

    ## IMPORTS
    import numpy as np
    import matplotlib.pyplot as plt
    import time
    import argparse

    # SETTING UP ARGPARSE
    parser = argparse.ArgumentParser(prog='Escape Time for a Photon through the Sun',
                                     description="Simulates the time distribution of a photon making it through some number of uniformly-dense slabs in 10 mean-free-path-lengths. Uses this time distribution to see how long it takes a random particle to diffuse the Sun which changes density as a function of the photon's radius. "
                                     "TOTAL RUN TIME: ~30-60 SECONDS")
    parser.add_argument("--N_slab",
                        type=int,
                        default=1000,  # meters
                        help="Type = Integer. The amount of runs used to get a probability distribution on the length of time it takes for a photon to make it through a slab of uniform density with a length of 10 mean free paths. Default value: 1000 runs.")
    parser.add_argument("--seed",
                        type=int,
                        default=12345,  # meters
                        help="Type = Integer. The seed used for generating random numbers. Default value: 12345")
    args = parser.parse_args()


    ## CONSTANTS
    R_sun = 696340000   # m
    R_sun_effective = 0.9 * R_sun  # m
    sigma_T = 6.652e-29  # Thomson cross-section, m^2
    n_init = 2.5 * 10**26 * 10**6  # electrons/cm^3 to electrons/m^3
    speed_c = 2.998 * 10**8  # m/s
    rng = np.random.default_rng(args.seed)

#########################################################################################
##############---1000 SIMULATIONS OF TRAVEL-TIME DISTRIBUTION---######################

    # initializing counting
    start = time.perf_counter()

    travel_times = []
    outcomes = []

    for i in range(args.N_slab):
        travel_time, outcome = simulate_slab()
        travel_times.append(travel_time)
        outcomes.append(outcome)

    travel_times = np.array(travel_times)
    outcomes = np.array(outcomes)

    end = time.perf_counter()

    # print results from the simulation
    print("---------RESULTS FOR 1000 SIMULATED SLABS---------")
    print("  Number of simulations:", args.N_slab)
    print("  Mean dimensionless travel time:", np.mean(travel_times))
    print("  Median dimensionless travel time:", np.median(travel_times))
    print("  Transmitted photons:", np.sum(outcomes == "transmitted"))
    print("  Reflected photons:", np.sum(outcomes == "reflected"))
    print(" **  Simulation time:", end - start, "seconds **")
    print("---------------------------------------------------")

    # plot travel-time distribution
    plt.figure(figsize=(9,6))
    plt.hist(travel_times, bins=80, density=True, edgecolor="black")
    plt.xlabel("Travel Time (mean free travel times)")
    plt.ylabel("Probability Density")
    plt.title("Photon Travel-Time Distribution Through 10 Mean Free Paths")
    plt.text(0.98,
             0.95,
             f"Number of Simulations = {args.N_slab}\n" f"Mean = {np.mean(travel_times):.2f}\n" f"Median = {np.median(travel_times):.2f}",
             transform=plt.gca().transAxes,
             fontsize=12,
             verticalalignment="top",
             horizontalalignment="right",
             bbox=dict(facecolor='lightblue', alpha=0.5, edgecolor='black'))  # textbox
    plt.show()


#########################################################################################
#####################---SIMULATE PHOTON GOING THROUGH SUN---#############################

    max_steps = 20000000000 # max number of diffusion steps for the photon to get through Sun
    scale_height = 0.096 * R_sun

    start2 = time.perf_counter()
    print("** TIMER STARTED **")
    escape_time, steps = simulate_solar_photon()
    end2 = time.perf_counter()
    print("** TIMER DONE **")

    # print MC results
    print(" ")
    print("---------RESULTS FOR PHOTON TRAVELLING THROUGH SUN---------")
    print("  Escape time:", escape_time / (60 * 60 * 24 * 365.25), "years")
    print("  Number of steps:", steps)
    print(" **  Simulation time:", end2 - start2, "seconds **")
    print("-----------------------------------------------------------")



