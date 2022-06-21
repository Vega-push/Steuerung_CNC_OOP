import matplotlib.pyplot as plt
import numpy as np

x = np.genfromtxt(fname="Lsg_0_5mm.txt", delimiter=",", skip_header=1, usecols=0)
y = np.genfromtxt(fname="Lsg_0_5mm.txt", delimiter=",", skip_header=1, usecols=1)

# x = np.linspace(0, 10, 200)
# y = np.sin(x)

# unterschiedliche Designmöglichkeiten
# plt.plot(x, y, "r--", x, y**2, "bs", x, y**3, "g^")
plt.plot(x, y, "r")
plt.grid()
# Grenzen für Achsen xmin, xmax, ymin, ymax
# plt.axis([0, 25, -1, 1])
plt.xlabel("Verfahrweg in mm")
plt.ylabel("B-Feld in Tesla")
plt.show()
