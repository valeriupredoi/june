import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def c_of_d(ys_orig, ys_line):
    """Compute the line R squared."""
    y_mean_line = [np.mean(ys_orig) for y in ys_orig]
    squared_error_regr = sum((ys_line - ys_orig) * (ys_line - ys_orig))
    squared_error_y_mean = sum((y_mean_line - ys_orig) * \
                               (y_mean_line - ys_orig))
    return 1 - (squared_error_regr / squared_error_y_mean)


def get_linear_parameters(x, y):
    """Retrive linear parameters."""
    # line parameters
    print("------ Analizying no of time points: {}".format(len(x)))
    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)

    # statistical parameters first line
    R = c_of_d(y, poly1d_fn(x))  # R squared
    y_err = poly1d_fn(x) - y  # y-error
    slope = coef[0]  # slope
    d_time = np.log(2.) / slope  # doubling time
    R0 = np.exp(slope) - 1.  # basic reproductive number, daily

    return poly1d_fn(x), R, y_err, slope, d_time, R0

pop_time = np.array([33., 40., 51., 57., ])
pop = np.array([63277., 94298., 141616., 168950., ])

lin_pars = get_linear_parameters(pop_time, pop)
plot_text = "Slope: %.2f pop/s;\ngoodness of fit: %.2f" % (lin_pars[3],
                                                           lin_pars[1]) 

plt.scatter(pop_time, pop)
plt.plot(pop_time, pop)
plt.grid()
plt.ylabel("Population size")
plt.xlabel("Time $generate\_world\_from\_geography()$ [s]")
plt.title("World generation: population vs runtime")
plt.text(35., 150000, plot_text, fontsize=9, color='k')
plt.savefig("../plots/world_creation_timing.png")
