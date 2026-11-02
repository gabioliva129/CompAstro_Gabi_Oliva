###
###  HW 5 Part 1  -- Monte Carlo Radiative Transfer
###
    # One of the most common uses of Monte Carlo calculations in astrophysics is for radiative transfer.
    # The simplest example of this is the motion of radiation in a star. The cores of stars are hot and dense,
    # such that all electrons are ionized and the cross-section for most photons to interact with an electron
    # is just the frequency independent Thompson cross-section.
    #
    # \sigma_T = \frac{8\pi}{3} \big(\frac{e^2}{4\pi \epsilon_0 m_e c^2}\big)^2  = 6.652 \times10^{-25} cm^2
    #
    # Another import quantity to consider in scattering theory is the mean free path of a particle:
    # l = 1/(n \times\sigma).  If n_e = 10^{20} cm^{-3} the mean free path would be 150m.
    #
    # Start by just considering a slab of constant electron density with this value and a width of 1km.
    # Perform a Monte Carlo simulation of a photon through this slab. Note that for low energy photons
    # (E = hf << m_e c^2) the photon scattering is isotropic, equally likely in any direction. However,
    # since you are only trying to follow the photons progress through the slab, you only need to
    # consider the angle the scattered photon makes with the direction through the slab.
    # Also note that your photon is almost as likely to be reflected back to the beginning
    # as make it through the slab, so make sure you account for this possibility. Make an
    # animation of your photon's path. One example of how to make an animation can be found here.

##########################################################################
## FUNCTIONS

def init():
    """blank initial function to set up the numpy animation"""
    line.set_data([], [])
    photon.set_data([], [])
    counter.set_text("")
    return line, photon, counter

def animate(i):
    """animation function that goes through each of the x and y points to
    create lines/position of the photon's path. it also counts how many steps
    of length=stepsize (default:50m) the system goes through before moving out
    of the slab """
    line.set_data(xpoints[:i+1], ypoints[:i+1])
    photon.set_data([xpoints[i]], [ypoints[i]])
    counter.set_text("Step: " + str(i))
    return line, photon, counter

##########################################################################

if __name__ == "__main__":

    ## IMPORTS
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import argparse

    # SETTING UP ARGPARSE
    parser = argparse.ArgumentParser(prog='Path of a Photon through a Slab of Electrons',
                                     description="Creates an animation of the motion of a photon's path through a constantly-dense 'slab' of electrons with width of 1.0 km. "
                                                 "Uses the probability of a photon to scatter in a given step size:    "
                                                 "p = 1 - e^(step_size * electron_density * Thomson_cross_section).    "
                                                 "Based on this probability to scatter, this code uses a Monte Carlo method to determine the photon's resulting path and in what"
                                                 "direction (assuming all angles for the photon to travel are equally-likely) until the photon leaves the slab of electron.")
    parser.add_argument("--step_size",
                        type=float,
                        default=50.0,  # meters
                        help="Type = Float. The step size, r, in unit of meters that the photon will travel within the electron slab (L=1000 m) in each step of the Monte Carlo. Value must be between 0 and 1000. Default value: 50.0 m.")
    parser.add_argument("--print_step_data",
                        action="store_true",
                        help="If present when running the file, data from each step of the Monte Carlo simulation will be printed. It will give details on if the photon is scattered at this step or not, the photon's initial position, the new direction the photon will travel if scattered, and the photon's new position after this step. Default: data are not printed.")
    args = parser.parse_args()


    ########################################################
    ## PARAMETERS
    sigma_T = 6.652e-25  # Thomson cross-section, cm^2
    n_e = 1e20   # e- density, cm^-3

    mfp = 1 / (n_e * sigma_T)
    mean_free_path = mfp / 100  # converting cm to meters

    L = 1000   # slab width, m
    ds = args.step_size    # step size, m  -- default = 50

    p = np.exp(-ds / mean_free_path)  # probability of *not* scattering over the step size

    print("Mean free path =", mean_free_path, "m")
    print("Step size =", ds, "m")
    print("Probability of scattering =", 1 - p)

    ########################################################
    ## SETTING UP INITIAL MOVEMENT/POSITION
    rng = np.random.default_rng()

    # initial position
    x = 0.0
    y = 0.0
    z = 0.0

    # initial direction (positive in the x-direction)
    vx = 1.0
    vy = 0.0
    vz = 0.0

    # stores positions for animation later
    xpoints = [x]
    ypoints = [y]
    zpoints = [z]

    # to count steps
    step_number = 0


    ########################################################
    ## SETTING UP MONTE CARLO LOOP
    print("------------------------------------------")
    while True:
        step_number += 1
        ############################################################
        # the following code determines if the photon is within a step size of one
        # of the boundaries, and stops the loop if the particle is heading out:
        if vx > 0:
            distance_to_boundary = (L-x) / vx
        elif vx < 0:
            distance_to_boundary = -x / vx
        else:
            distance_to_boundary = np.inf

        # determines if a full step_size (default:50m) fits inside the slab
        if distance_to_boundary <= ds:

            # final partial step to the boundary
            x += distance_to_boundary * vx
            y += distance_to_boundary * vy
            z += distance_to_boundary * vz

            xpoints.append(x)
            ypoints.append(y)
            zpoints.append(z)

            if args.print_step_data:
                print("\nStep", step_number)
                print(f"Final partial step: {distance_to_boundary:.2f} m")
                print("Photon reaches a slab boundary.")

            if x >= L:
                outcome = "TRANSMITTED"
                if args.print_step_data:
                    print("Photon exits through the opposite side!")

            else:
                outcome = "REFLECTED"
                if args.print_step_data:
                    print("Photon exits through the entrance side!")

            break
        ################################

        R = rng.random()

        if args.print_step_data:
            print("\nStep", step_number)
            print(f"Position before step = {float(x):.2f}, {float(y):.2f}, {float(x):.2f}")
            print("Random number =", round(R, 4))

        ## SEE IF PHOTON SCATTERS OR NOT -- scatters if R>p_not_scattering, continues if R<p_not_scattering

        if R > p:
            if args.print_step_data:
                print("ACTION: PHOTON SCATTERS")

            # photon moves stepsize (default:50m) in its current direction
            x += ds * vx
            y += ds * vy
            z += ds * vz

            # generates random numbers for random angles
            R_theta = rng.random()
            R_phi = rng.random()

            # scattering
            theta = np.arccos(2 * R_theta - 1) # theta goes from -pi/2 to +pi/2
            phi = 2 * np.pi * R_phi  # phi goes from 0 to 2pi radians

            # converts angles to degrees for simpler reading when printed
            theta_deg = np.degrees(theta)
            phi_deg = np.degrees(phi)

            # calculates new 3D velocity direction with the randomly-generated scattering angles
            vx = np.cos(theta)
            vy = np.sin(theta) * np.cos(phi)
            vz = np.sin(theta) * np.sin(phi)

            if args.print_step_data:
                print("   Theta =", round(theta_deg, 2), "degrees")
                print("   Phi =", round(phi_deg, 2), "degrees")

                print("New direction:")
                print("   vx =", round(vx, 4))
                print("   vy =", round(vy, 4))
                print("   vz =", round(vz, 4))

                if vx > 0:
                    print("Photon now travels FORWARD.")

                elif vx < 0:
                    print("Photon now travels BACKWARD.")

                else:
                    print("Photon travels parallel to the slab's boundaries.")

        else:  # i.e.  if R < p
            if args.print_step_data:
                print("ACTION: PHOTON CONTINUES WITHOUT SCATTERING")

            # move the particle a step_size (default:50m) in the direction it's currently traveling
            x += ds * vx
            y += ds * vy
            z += ds * vz

        # store the new position for the animation
        xpoints.append(x)
        ypoints.append(y)
        zpoints.append(z)

        if args.print_step_data:
            print(f"New position = {float(x):.2f}, {float(y):.2f}, {float(x):.2f}")


    ## PRINT FINAL OUTCOME
    print("------------------------------------------")
    print("Total steps =", step_number)
    print(f"Final position = {float(x):.2f}, {float(y):.2f}, {float(x):.2f}")
    print("Final outcome =", outcome)


    ########################################################
    ## MAKING THE PLOT AND ANIMATION
    fig, ax = plt.subplots(figsize=(10, 6))

    xmin = min(xpoints) - ds
    xmax = max(xpoints) + ds
    ymin = min(ypoints) - ds
    ymax = max(ypoints) + ds
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_xlabel("x-position (m)")
    ax.set_ylabel("y-position (m)")
    ax.set_title("3D Monte Carlo Photon Path (2D Projection)")

    prob_percent = (1-p)*100
    ax.text(0.02, 0.9,f"Probability of Scattering: {prob_percent:.2f}%",transform=ax.transAxes)

    # drawing the slab
    ax.axvline(0, color="red", linestyle="--", label="Entrance")
    ax.axvline(L, color="red", linestyle=":", label="Exit")
    ax.axvspan(0, L, color="pink", alpha=0.3)

    # tracing the particle's path
    line, = ax.plot([], [], "*-", linewidth=1.5)
    photon, = ax.plot([], [], "ro", markersize=8)
    counter = ax.text(0.02, 0.95, "", transform=ax.transAxes)  # step counter

    ax.legend()


    # produces animation
    ani = animation.FuncAnimation(fig, animate, frames=len(xpoints), init_func=init, interval=300, blit=True)

    # saving the animation
    writer = animation.PillowWriter(fps=4)
    ani.save("HW_5_3D_photon_scattering.gif", writer=writer)

    plt.show()


