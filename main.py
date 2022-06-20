from maschine import Connection, Maschine
from gui import Gui

# connection = Connection()
# maschine = Maschine(connection.steuerung)
gui = Gui()
print(gui.FONT)
gui.mainloop()

# maschine.steuerung.moveTo(0, 350000, 1500)
# while not (maschine.steuerung.positionReached(0)):
#     pass
# maschine.steuerung.moveTo(0, 0, 1500)
# while not (maschine.steuerung.positionReached(0)):
#     pass

