import PyTrinamic
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM3110.TMCM_3110 import TMCM_3110
from cebomsr import LibraryInterface, DeviceType


class Connection:
    """
    starte Verbindung mit der Maschine und lege ein Steuerungsobjekt an
    """

    def __init__(self):
        # Connection Motorcontroller
        PyTrinamic.showInfo()
        self.connection_manager_TMCM6110 = ConnectionManager()
        self.interface_TMCM6110 = self.connection_manager_TMCM6110.connect()
        self.steuerung = TMCM_3110(self.interface_TMCM6110)
        print("connection TMCM6110 start")
        # Connection Cebo
        self.devices = LibraryInterface.enumerate(DeviceType.CeboLC)
        self.cebo = None
        self.connect_cebo()
        print("connection CEBO start")

    def __del__(self):
        self.interface_TMCM6110.close()
        print("connection TMCM6110 close")
        self.cebo.close()
        print("connection CEBO close")

    def connect_cebo(self):
        if len(self.devices) > 0:
            self.cebo = self.devices[0]
            self.cebo.open()

    def messwert_auslesen(self):
        value_0 = self.cebo.getSingleEndedInputs()[1].read()
        value_1 = self.cebo.getSingleEndedInputs()[0].read()
        value = value_1 - value_0
        return value


