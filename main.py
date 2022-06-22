from maschine import Maschine
from connection import Connection
from gui import Gui


def main():
    # stelle Verbindungen her
    connection = Connection()
    # erstelle Maschinenobjekt
    maschine = Maschine(connection.steuerung, connection)
    # erstelle User-Interface
    gui = Gui(maschine)
    # Endlosschleife für User-Interface
    gui.mainloop()


# main() wird nur verwendet, wenn das Programm nicht als Modul geladen wird
if __name__ == "__main__":
    main()
