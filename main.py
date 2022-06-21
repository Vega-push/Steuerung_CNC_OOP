from maschine import Maschine
from connection import Connection
from gui import Gui

connection = Connection()
maschine = Maschine(connection.steuerung, connection)
gui = Gui(maschine)

gui.mainloop()

# maschine.steuerung.moveTo(0, 350000, 1500)
# while not (maschine.steuerung.positionReached(0)):
#     pass
# maschine.steuerung.moveTo(0, 0, 1500)
# while not (maschine.steuerung.positionReached(0)):
#     pass

