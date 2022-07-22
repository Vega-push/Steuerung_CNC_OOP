import matplotlib.pyplot as plt
import numpy as np


def plot_ausgeben(filename):
    """
    Die Funktionen plottet die bei der Messung erzeugten Messergebnisse.
    Bei der Funktion np.genfromtext kann mit dem Parameter usecols die gewünschte Zeile
    ausgewählt werden zum plotten. Zählweise startet bei 0.
    :param filename: Usereingabe Name der Messdatei wird übergeben
    :return: None
    """
    x = np.genfromtxt(fname=filename, delimiter=",", skip_header=1, usecols=0)
    y = np.genfromtxt(fname=filename, delimiter=",", skip_header=1, usecols=6)
    plt.plot(x, y, "r")
    plt.grid()
    plt.xlabel("Messpunkte")
    plt.ylabel("B-Feld in Tesla")
    plt.show()


if __name__ == "__main__":
    plot_ausgeben("messung1.csv")
