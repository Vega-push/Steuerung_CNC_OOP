import PyTrinamic
import configparser
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM3110.TMCM_3110 import TMCM_3110


class Connection:
    """
    starte Verbindung mit der Maschine und lege ein Steuerungsobjekt an
    """

    def __init__(self):
        PyTrinamic.showInfo()
        self.connection_manager_TMCM6110 = ConnectionManager()
        self.interface_TMCM6110 = self.connection_manager_TMCM6110.connect()
        self.steuerung = TMCM_3110(self.interface_TMCM6110)
        print("connection start")

    def __del__(self):
        self.interface_TMCM6110.close()
        print("connection close")


class Maschine:
    """
    lese Config-Daten ein und lege ein Maschinenobjekt an welches die:
    steuerung
    antriebsdaten --> von config
    achsparameter --> von config
    enthält
    """
    def __init__(self, connection):
        self.steuerung = connection
        self.antrieb = None
        self.achsen_prm = None
        self.einlesen_config_daten()
        self.setze_achsparameter()

    def einlesen_config_daten(self) -> None:
        """
        laden und abspeichern der Config.ini Datei in dictionaries
        :return: None
        """
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.achsen_prm = {key: value for (key, value) in config["Achsenparameter"].items()}
        self.antrieb = {key: value for (key, value) in config["Antriebsstrang"].items()}

    def setze_achsparameter(self) -> None:
        """
        setzen der Achsenparameter fuer alle verfuegbaren Achsen
        :return: None
        """
        for i in range(self.steuerung.MOTORS):
            # print(f"fuer die Achse{i}: ")
            for key, value in self.achsen_prm.items():
                # print(f"Achsenparameter {key}, Wert {value}.")
                self.steuerung.setAxisParameter(apType=int(key), motor=i, value=int(value))

    def ausgabe_ap(self) -> None:
        """
        Ausgabe aller eingestellten Achsparameter für alle Achsen
        :return: None
        """
        for i in range(self.steuerung.MOTORS):
            print(f"Achse {i}:")
            for key in self.achsen_prm:
                print(self.steuerung.getAxisParameter(int(key), i))

    def np_referenzfahrt(self) -> None:
        # fahre jede Achse gegen Referenzschalter und setze NP
        achsen = [value for (key, value) in self.antrieb.items() if key == "y_achse"
                  or key == "x_achse" or key == "z_achse"]
        for achse in range(self.steuerung.MOTORS):
            self.steuerung.rotate(achse, 1500)
            while not (self.steuerung.getAxisParameter(10, achse)):  # 10 =right limit switch state
                pass
            self.steuerung.stop(achse)
            # fahre max Achsenverfahrweg vom Schalter zurueck
            self.steuerung.moveBy(achse, -1 * int(achsen[achse]), 1500)
            while not (self.steuerung.positionReached(achse)):
                pass
            self.steuerung.stop(achse)
            # NP setzen
            self.steuerung.setAxisParameter(apType=1, motor=achse, value=0)

    def pps_in_mm(self, achse, vpps) -> float:
        """
        Rotatorische Bewegung (pps) in eine translatorische Bewegung (mm).
        :param achse: Achsparameter werden anhand der Achse ausgelesen [int]
        :param vpps: Weg in pps der umgerechnet werden soll [int]
        :return: Verfahrweg in mm [float]
        """
        vollschritt = float(self.antrieb["vollschritt"])
        mic_step_res = 2 ** self.steuerung.getAxisParameter(140, achse)
        steigung = float(self.antrieb["steigung_mm_pro_u"])
        uebersetzung = float(self.antrieb["getriebe_uebersetzung"])
        return round(((vpps / ((360 / vollschritt) * mic_step_res)) * steigung * uebersetzung), 3)

    def mm_in_pps(self, achse, strecke) -> int:
        """
        Translatorische Bewegung (mm) in rotatorische Bewegung umrechnen(pps)
        :param achse: Achparameter werden anhand der Achse ausgelesen [int]
        :param strecke: Weg in mm der umgerechnet werden soll [float]
        :return: Verfahrweg in pps [int]
        """
        vollschritt = float(self.antrieb["vollschritt"])
        mic_step_res = 2 ** self.steuerung.getAxisParameter(140, achse)
        steigung = float(self.antrieb["steigung_mm_pro_u"])
        uebersetzung = float(self.antrieb["getriebe_uebersetzung"])
        return int((strecke * (360 / vollschritt) * mic_step_res) / (steigung * uebersetzung))

    def manual_mode(self, achse, richtung, speed):
        """Achse verfährt so lange, wie der Knopf gedrückt ist"""
        if richtung == "+":
            self.steuerung.rotate(achse.get(), speed.get())
        elif richtung == "-":
            self.steuerung.rotate(achse.get(), speed.get() * -1)

    def stop_manual_mode(steuerung, achse, text, antriebsstrang):
        """Knopf loslassen, um Achse zu stoppen"""
        achsen_verfahrwege = {
            "0": antriebsstrang["y_max_weg"],
            "1": antriebsstrang["x_max_weg"],
            "2": antriebsstrang["z_max_weg"]
        }
        steuerung.stop(achse.get())
        # aktuelle Position und max. Weg je nach Achse im Textfeld anzeigen
        akt_pos = steuerung.getAxisParameter(1, achse.get())
        text.delete(1.0, "end")
        # Ueberlaufproblem mit Achsparameter 1 aktuelle Position
        if akt_pos > 2147483647:
            akt_pos = 0
        text.insert("end",
                    f"aktuelle Position: {akt_pos}pps = {pps_in_mm(steuerung, antriebsstrang, achse.get(), akt_pos)}mm\n")
        text.insert("end", "maximaler Weg von 0 - " + achsen_verfahrwege[str(achse.get())] + "pps")
