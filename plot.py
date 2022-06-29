import matplotlib.pyplot as plt
import numpy as np


def plot_ausgeben(filename):
    x = np.genfromtxt(fname=filename, delimiter=",", skip_header=1, usecols=0)
    y = np.genfromtxt(fname=filename, delimiter=",", skip_header=1, usecols=6)
    plt.plot(x, y, "r")
    plt.grid()
    plt.xlabel("Messpunkte")
    plt.ylabel("B-Feld in Tesla")
    plt.show()