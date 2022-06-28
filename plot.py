import matplotlib.pyplot as plt
import numpy as np


def plot_ausgeben():
    x = np.genfromtxt(fname="messung2.csv", delimiter=",", skip_header=1, usecols=0)
    y = np.genfromtxt(fname="messung2.csv", delimiter=",", skip_header=1, usecols=6)
    plt.plot(x, y, "r")
    plt.grid()
    plt.xlabel("Verfahrweg in mm")
    plt.ylabel("B-Feld in Tesla")
    plt.show()