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
        value_list_1 = []
        value_list_0 = []
        # Anzahl der Wiederholungen definiert die Messanzahl an einem Messpunkt
        for _ in range(10):
            value_list_0.append(self.cebo.getSingleEndedInputs()[1].read())
            value_list_1.append(self.cebo.getSingleEndedInputs()[0].read())
        mean_0 = sum(value_list_0) / len(value_list_0)
        mean_1 = sum(value_list_1) / len(value_list_1)
        value = mean_1 - mean_0
        return value


