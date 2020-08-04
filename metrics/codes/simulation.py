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

pop_time = np.array([80., 103., 136., 162., ])
pop = np.array([81875., 107422., 141616., 168950., ])
mem = np.array([125., 132., 145., 160., ])

lin_pars_t = get_linear_parameters(pop_time, pop)
lin_pars_mem = get_linear_parameters(mem, pop)
plot_text_t = "Time\nSlope: %.2f pop/s;\ngoodness of fit: %.2f" % (lin_pars_t[3],
                                                                   lin_pars_t[1])
plot_text_mem = "Memory\nSlope: %.2f pop/10M;\ngoodness of fit: %.2f" % (lin_pars_mem[3],
                                                                       lin_pars_mem[1])

plt.scatter(pop_time, pop, label="time")
plt.plot(pop_time, pop)
plt.scatter(mem, pop, label="mem")
plt.plot(mem, lin_pars_mem[0])
plt.grid()
plt.ylabel("Population size")
plt.xlabel("Time[s]/maxMem[10M] $simulator.run()$")
plt.title("Simulator: population vs runtime/maxMem (20 days)")
plt.text(80., 150000, plot_text_t, fontsize=9, color='k')
plt.text(80., 130000, plot_text_mem, fontsize=9, color='k')
plt.legend()
plt.savefig("../plots/simulator_timing.png")
