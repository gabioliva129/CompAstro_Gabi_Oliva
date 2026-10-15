"""
HW4 – Fourier Analysis – Time Series Analysis

Many astrophysical phenomena very over short enough time scales that they can be observed by humans. One of the strongest
time varying signals are occulting binaries, when two orbiting stars pass in front of one-another. This website has data
from the TESS machine that observed hundreds of nearby stars. You can download the data for a light curve as a fits file
from the site after you choose a star. You can read the file using astropy.


Note that these files contain errors on the measured fluxes that we will not use in Fourier analysis. If you plot a
light curve you’ll see that these observations have lots of points and then a long time and then lots of points. This is
how the observations were done, with the telescope on the object for some set amount of time and then revisiting the object
many months or years later. Choose an epoch with lots of observations and reduce your data to just that range. Create the
Fourier transform for that range and plot the power spectrum. See how few coefficients you can use to capture the behavior
of the eclipsing binary looking at the inverse transform. You can check a different region of the light curve and redo the
analysis to see if you get the same results.

An extra complication. The TESS data is almost evenly spaced. The observations were done evenly spaced, but there will
be some missing data because things happen. If you look at the times in the file, you can identify the missing time steps.
You can try filling this in with linear interpolation and then redoing the Fourier analysis. Because the TESS data is so good,
this won’t make much of a difference. If the light curve was much more unevenly sampled the Fourier transform would be totally
wrong. This is how most astronomy data is and dealing with those problems is what much of time series analysis is about.
"""


###################################################################################################################
### FUNCTIONS!

# DEFINE FOURIER TRANSFORM
def dft(y):      # this returns only the non-negative-frequency coefficients
    N = len(y)
    c = np.zeros(N//2+1, complex)
    for k in range(N//2+1):
        for n in range(N):
            c[k] += y[n] * np.exp(-2j * np.pi * k * n / N)
    return c



# DEFINE INVERSE FOURIER TRANSFORM
def inverse_dft(c, N):
    y_new = np.zeros(N, dtype=float)
    for n in range(N):
        total = c[0].real
        for k in range(1, (N + 1)//2):  # positive frequencies
            total += 2 * np.real(c[k] * np.exp(2j * np.pi * k * n / N))
        if N % 2 == 0:   # include the highest frequency peak once for even numbers (b/c equal to half of the sampling rate)
            total += c[N//2].real * (-1)**n
        y_new[n] = total / N
    return y_new

###################################################################################################################

if __name__ == "__main__":
    # IMPORTS
    from astropy.io import fits
    import numpy as np
    import argparse
    from matplotlib import pyplot as plt


    # SETTING UP ARGPARSE
    parser = argparse.ArgumentParser(prog='Finding Frequencies of Star Eclipses in TESS',
                                     description="Runs an Inverse Fourier Transform to find model the repetivite light curves of stars.")

    parser.add_argument("--display_star_data",
                        type=bool,
                        default=True,
                        help="Type = Boolean. If True, a plot of the original light curve data from the 0458461293 Star from TESS is displayed. Default is True (plot is displayed).")

    parser.add_argument("--display_fourier",
                        type=bool,
                        default=True,
                        help="The initial, total Fourier Transform of the star data on top of the data. Also, the power spectrum of the total Fourier analysis, showing the weight of the different coefficients. Default is True (plot is displayed).")

    parser.add_argument("--reconstruction",
                        type=bool,
                        default=False,
                        help="Type = Boolean. When True, this will display a plot of the reconstructed Fourier transform of the original star data. It is a recreation of the original data with the coefficients accounting 75 percent of the total weight of the coefficients. Also, it will display the power spectrum of this reconstruction, showing how the most influential values from the total Fourier transform were kept. Lastly, the values of these coefficients will be printed. Default is False (graphs/values are not displayed).")

    parser.add_argument("--power_value",
                        type=float,
                        default=0.5,
                        help="Type = Float. The desired fraction of the power spectrum to be included in the reconstructed data with less coefficients. Values are from 0 to 1. The closer to 1, the more accurate the transform, and the more coefficients included. Default value is 0.5.")

    args = parser.parse_args()




    # EXTRACTING DATA
    hdul = fits.open("tic0458461293.fits")
    times = hdul[1].data['times']
    fluxes = hdul[1].data['fluxes']
    ferrs = hdul[1].data['ferrs']



    # PICKING A SECTION OF THE DATA
    fluxes_trunc = fluxes[(times>=1870) & (times<=1926)]
    times_trunc = times[(times>=1870) & (times<=1926)]
    # print(len(fluxes))
    # print(len(fluxes_trunc))




    # DISPLAY ORIGINAL STAR LIGHT CURVE
    if args.display_star_data == True:
        plt.figure(figsize=(18,9))
        plt.plot(times_trunc, fluxes_trunc)
        # plt.axhline(y=1, color='red', alpha=0.5)
        plt.xlabel("Time")
        plt.ylabel("Flux")
        plt.title("TESS Light Curve of 0458461293 (at selected interval)")
        plt.grid(alpha=0.3)
        plt.scatter(times_trunc, fluxes_trunc, s=5, color='black')
        plt.show()



    # FOURIER TRANSFORM GRAPH AND POWER SPECTRUM
    mean_flux = np.mean(fluxes_trunc)
    y_vals = fluxes_trunc - mean_flux
    c1 = dft(y_vals)

    if args.display_fourier == True:
        y_reconstructed = inverse_dft(c1, len(y_vals)) + mean_flux

        fig, axes = plt.subplots(2, 1, figsize=(16, 9))

        # PLOTTING RECONSTRUCTED PLOT FROM FOURIER COEFFICIENTS
        axes[0].plot(times_trunc, fluxes_trunc, ".", markersize=3, label="Data")
        axes[0].plot(times_trunc, y_reconstructed, label="Inverse DFT")
        axes[0].set_xlabel("Time")
        axes[0].set_ylabel("Flux")
        axes[0].set_title("Full Fourier Light Curve Reconstruction")
        axes[0].legend()
        axes[0].grid(alpha=0.3)

        # PLOTTING POWER SPECTRUM
        axes[1].plot(np.abs(c1) ** 2)
        axes[1].plot(np.abs(c1) ** 2, "r.",markersize=4)
        axes[1].set_xlabel("Fourier Coefficient k")
        axes[1].set_ylabel(r"$|c_k|^2$")
        axes[1].set_title("Power Spectrum")
        axes[1].grid(alpha=0.3)

        plt.tight_layout()
        plt.show()




    # RECONSTRUCTING THE GRAPH WITH FEWER COEFFICIENTS
    power_spec = np.abs(c1) ** 2
    sorted_indices = np.argsort(power_spec)[::-1]  # sorts them from highest coefficient to lowest

    total_power = np.sum(power_spec)
    cumulative_power = 0
    n_keep = 0

    while cumulative_power < args.power_value * total_power:  # keep adding coefficients until reaching user-given fraction of total power in the spectrum (default=0.75)
        cumulative_power += power_spec[sorted_indices[n_keep]]
        n_keep += 1   # n_keep will be the number of coefficients needed to recreate the graph to the given threshold

    top_indices = sorted_indices[:n_keep]



    c_only_top = np.zeros_like(c1)  # creates a complex array of zeros
    c_only_top[top_indices] = c1[top_indices]   # power spectrum is all zeros except for the selected highest coefficients in their correct place

    y_less_coeff = inverse_dft(c_only_top, len(y_vals)) + mean_flux




    # DISPLAYING THE VALUES/GRAPH WITH FEWER COEFFICIENTS
    if args.reconstruction == True:
        print(" ")
        print(f"Number of coefficients kept for {args.power_value} of power: ", n_keep)
        # print("Fraction of total power retained:", cumulative_power / total_power)

        # print("Top coefficient indices:", top_indices)
        print("Values of the 10 highest coefficient powers:", power_spec[top_indices][:10])



        fig, axes = plt.subplots(2, 1, figsize=(16, 9))

        # DISPLAY RECONSTRUCTED LIGHT CURVE WITH FEWER COEFFICIENTS
        axes[0].plot(times_trunc, fluxes_trunc, "b", label="Data")
        axes[0].plot(times_trunc, y_reconstructed, "r", label="Inverse DFT")
        axes[0].set_xlabel("Time")
        axes[0].set_ylabel("Flux")
        axes[0].set_title(f"Reconstruction Using the {n_keep} Most Powerful Coefficients")
        axes[0].legend()
        axes[0].grid(alpha=0.3)

        # POWER SPECTRUM OF THE RECONSTRUCTED CURVE WITH FEWER COEFFICIENTS
        axes[1].plot(np.abs(c_only_top) ** 2)  # plotting the line
        axes[1].plot(np.abs(c_only_top) ** 2, 'r.', markersize=1)  # plotting the points
        axes[1].set_xlabel("Fourier Coefficient k")
        axes[1].set_ylabel(r"$|c_k|^2$")
        axes[1].set_title("Power Spectrum")
        axes[1].grid(alpha=0.3)

        plt.tight_layout()
        plt.show()