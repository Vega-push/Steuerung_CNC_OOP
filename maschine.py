import configparser
import time
import csv
from tkinter import simpledialog
from tkinter import messagebox


class Maschine:
    """
    lese Config-Daten ein und lege ein Maschinenobjekt an welches die:
    steuerung
    antriebsdaten → von config
    achsparameter → von config
    enthält
    """
    def __init__(self, connection, cebo):
        self.steuerung = connection
        self.cebo = cebo
        self.messdaten = []
        self.index = 0
        self.antrieb = None
        self.achsen_prm = None
        self.std_np = [0, 0, 0]
        self.skript = None
        self.einlesen_config_daten()
        self.setze_achsparameter()
        self.achsen_max = [value for (key, value) in self.antrieb.items()
                           if key == "y_achse" or key == "x_achse" or key == "z_achse"]

    def einlesen_config_daten(self):
        """
        laden und abspeichern der Config.ini Datei in dictionaries
        :return: None
        """
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.achsen_prm = {key: value for (key, value) in config["Achsenparameter"].items()}
        self.antrieb = {key: value for (key, value) in config["Antriebsstrang"].items()}

    def setze_achsparameter(self):
        """
        setzen der Achsenparameter fuer alle verfuegbaren Achsen
        :return: None
        """
        for i in range(self.steuerung.MOTORS):
            for key, value in self.achsen_prm.items():
                self.steuerung.setAxisParameter(apType=int(key), motor=i, value=int(value))

    def ausgabe_ap(self):
        """
        Debug-Funktion zur Ausgabe aller eingestellten Achsparameter für alle Achsen
        :return: None
        """
        for i in range(self.steuerung.MOTORS):
            print(f"Achse {i}:")
            for key in self.achsen_prm:
                print(self.steuerung.getAxisParameter(int(key), i))

    def np_referenzfahrt(self):
        """
        Referenzfahrt für alle verfügbaren Achsen, jede Achse wird in den Endschalter gefahren,
        von hier wird in die gegenüberliegende Richtung um einen fest in der config.ini gesetzten Betrag verfahren,
        am Ziel angekommen wird der Nullpunkt gesetzt
        :return:
        """
        # Zuerst die z-Achse aus dem Weg fahren
        self.steuerung.rotate(2, 2000)
        while not (self.steuerung.getAxisParameter(10, 2)):  # 10 =right limit switch state
            pass
        self.steuerung.stop(2)
        # fahre jede Achse gegen Referenzschalter und setze NP
        for achse in range(self.steuerung.MOTORS):
            self.steuerung.rotate(achse, 2000)
            while not (self.steuerung.getAxisParameter(10, achse)):  # 10 =right limit switch state
                pass
            self.steuerung.stop(achse)
            # fahre max Achsenverfahrweg vom Schalter zurueck
            self.steuerung.moveBy(achse, -1 * int(self.achsen_max[achse]), 2000)
            while not (self.steuerung.positionReached(achse)):
                pass
            self.steuerung.stop(achse)
            # NP setzen
            self.steuerung.setAxisParameter(apType=1, motor=achse, value=0)
            if achse == 2:
                self.steuerung.rotate(achse, 2000)
                while not (self.steuerung.getAxisParameter(10, achse)):  # 10 =right limit switch state
                    pass
                self.steuerung.stop(achse)
        self.setze_achsparameter()

    def setze_resette_np(self, button):
        """
        Setze oder resette die NP der Achsen an der aktuellen Position.
        Bevor NP's gesetzt werden, wird die aktuelle Achsposition gepseichert,
        um später die standardmäßigen NP's wiederherstellen zu können.
        :param button: gui-widget
        :return: None
        """
        if button["text"] == "NP setzen":
            # lese aktuelle NP-Werte ein
            self.std_np = [self.steuerung.getAxisParameter(1, 0),
                           self.steuerung.getAxisParameter(1, 1),
                           self.steuerung.getAxisParameter(1, 2)]
            # setze neue NP's
            for achse in range(self.steuerung.MOTORS):
                self.steuerung.stop(achse)
                self.steuerung.setAxisParameter(apType=1, motor=achse, value=0)
            button["text"] = "NP resetten"
        elif button["text"] == "NP resetten":
            # resette Nullpunkt
            # fahre auf x, y, z = 0 und setze achsposition auf self.xyz-wert
            for achse in range(self.steuerung.MOTORS):
                self.steuerung.moveTo(achse, 0, 1500)
                while not (self.steuerung.positionReached(achse)):
                    pass
                self.steuerung.stop(achse)
                self.steuerung.setAxisParameter(apType=1, motor=achse, value=self.std_np[achse])
            button["text"] = "NP setzen"

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
        """
        Achse verfährt so lange, wie der Knopf gedrückt ist
        :param achse: Achsenauswahl
        :param richtung: Richtungsauswahl
        :param speed: Verfahrgeschwindigkeit
        :return: None
        """
        if richtung == "+":
            self.steuerung.rotate(achse.get(), speed.get())
        elif richtung == "-":
            self.steuerung.rotate(achse.get(), speed.get() * -1)

    def stop_manual_mode(self, achse, text):
        """
        Knopf loslassen, um Achse zu stoppen
        :param achse: Achsenauswahl
        :param text: Übergabe gui-widget
        :return:
        """
        achsen_verfahrwege = {
            "0": self.antrieb["y_achse"],
            "1": self.antrieb["x_achse"],
            "2": self.antrieb["z_achse"]
        }
        self.steuerung.stop(achse.get())
        # aktuelle Position und max. Weg je nach Achse im Textfeld anzeigen
        akt_pos = self.steuerung.getAxisParameter(1, achse.get())
        text.delete(1.0, "end")
        # Ueberlaufproblem mit Achsparameter 1 aktuelle Position
        if akt_pos > 2147483647:
            akt_pos -= 4294967296
        text.insert("end", f"aktuelle Position: {akt_pos}pps = {self.pps_in_mm(achse.get(), akt_pos)}mm\n")
        text.insert("end", f"maximaler Weg von 0 - {achsen_verfahrwege[str(achse.get())]}pps ="
                           f" {self.pps_in_mm(achse.get(), int(achsen_verfahrwege[str(achse.get())]))}mm")

    def skript_ausfuehren(self, single_mode, skriptbox):
        """
        Ausführen des Skriptes im Editor
        :param single_mode: Einzelschrittbetrieb ja/nein
        :param skriptbox: Übergabe gui-widget
        :return: None
        """
        # skirpt einlesen erfolgreich?
        if self.skript_einlesen(skriptbox):
            # Einzelschrittbetrieb aktiviert?
            if single_mode.get():
                # Befehl für Befehl abarbeiten
                for i, reihe in enumerate(self.skript):
                    skriptbox.tag_add("start", f"{i + 1}.0", f"{i + 1}.end")
                    skriptbox.tag_config("start", background="red", foreground="white")
                    skriptbox.update()
                    self.befehlsauswahl(reihe)
                    # zeige Box erst nach Wartebefehl, somit keine Bestätigung vor Beenden der Bewegung möglich
                    if reihe[0] == "WAIT":
                        msg_box = messagebox.askquestion(title="Schrittbetrieb",  message="Fortfahren?")
                        if msg_box == "yes":
                            pass
                        else:
                            skriptbox.tag_delete("start")
                            break
                skriptbox.tag_delete("start")
            else:
                # Befehl für Befehl abarbeiten
                for i, reihe in enumerate(self.skript):
                    skriptbox.tag_add("start", f"{i + 1}.0", f"{i + 1}.end")
                    skriptbox.tag_config("start", background="red", foreground="white")
                    skriptbox.update()
                    self.befehlsauswahl(reihe)
                skriptbox.tag_delete("start")
            self.messdaten_schreiben(self.messdaten)

    def skript_einlesen(self, skriptbox) -> bool:
        """
        Lese den Inhalt der skriptbox, bereite Daten auf, überprüfe das Skript auf Fehler,
        falls das Skript in Ordnung ist speichere es ab.
        :param skriptbox: Übergabe um auf Daten des Textfelds zuzugreifen
        :return: bool
        """
        inhalt = skriptbox.get(1.0, "end").strip()
        string_inhalt = [[string.strip().upper()] for string in inhalt.split("\n")]
        skript = [word.strip().split(",") for string in string_inhalt for word in string]
        flag_skript, zeile = self.skript_ueberpruefen(skript)
        if flag_skript:
            self.skript = skript
            return True
        else:
            messagebox.showinfo(message=f"Fehler im Skript in Zeile {zeile}!\n")
            return False

    @staticmethod
    def skript_ueberpruefen(skript):
        """
        durchsuche das übergebene Skript nach Fehlern und gebe die Zeile des
        ersten gefunden Fehlers zurück
        :param skript: gui-widget
        :return: bool, int=Zeilennummer vom Fehler
        """
        # konstante Variablen abspeichern
        befehlsliste = ["MVP", "WAIT", "ROR", "ROL", "MST", "SAP", "GAP", "SIO", "GIO", "LOOP"]

        # jeden Befehl jeder Zeile überprüfen, bei Fehler Rückgabe False und Zeilennr.
        for i, zeile in enumerate(skript):
            if zeile[0] in befehlsliste:
                pass
            else:
                return False, i + 1
        return True, 0

    def befehlsauswahl(self, alte_zeile):
        """
        Compiler für Skripte, wählt passenden Befehl je nach Eingabe aus
        :param alte_zeile: Befehlszeile
        :return: None
        """
        # Formatierung Befehl
        zeile = []
        for string in alte_zeile:
            new_string = string.strip()
            zeile.append(new_string)
        befehl = zeile[0]

        # Auswahl Befehlssatz
        match befehl:
            case "MVP":
                befehlstyp = zeile[1]
                achse = int(zeile[2])
                verfahrweg = int(zeile[3])
                if befehlstyp == "ABS":
                    if self.verfahrgrenze_ueberpruefen(zeile, self.achsen_max[achse]):
                        self.steuerung.moveTo(motor=achse, position=verfahrweg)
                    else:
                        print("Verfahrgrenzen nicht eingehalten!")
                        exit()
                elif befehlstyp == "REL":
                    if self.verfahrgrenze_ueberpruefen(zeile, self.achsen_max[achse]):
                        self.steuerung.moveBy(motor=achse, difference=verfahrweg)
                    else:
                        print("Verfahrgrenzen nicht eingehalten!")
                        exit()
            case "WAIT":
                achse = int(zeile[2])
                while not (self.steuerung.positionReached(achse)):
                    pass
                # wenn Position erreicht ist, Sensor auslesen
                self.messdaten_updaten()
            case "ROR":
                achse = int(zeile[1])
                velocity = int(zeile[2])
                verfahrzeit = float(zeile[3])
                v_pps = (16 * 10 ** 6 * velocity) / (2 ** self.steuerung.getAxisParameter(154, achse) * 2048 * (
                            2 ** self.steuerung.getAxisParameter(140, achse)))
                aktuelle_pos = self.steuerung.getAxisParameter(1, achse)
                max_weg = int(self.achsen_max[achse]) - aktuelle_pos
                max_verfahrzeit = int(max_weg / v_pps) - 1  # Sicherheitspuffer
                if max_verfahrzeit > verfahrzeit:
                    self.steuerung.rotate(motor=achse, velocity=velocity)
                    time.sleep(verfahrzeit)
                    self.steuerung.stop(achse)
                    # wichtig!!! nach ROR sonst kein MVP mehr möglich, überschreiben
                    # des AP-s aktuelle Pos
                    self.setze_achsparameter()
                else:
                    print("Verfahrzeit zu groß!")
            case "ROL":
                achse = int(zeile[1])
                velocity = int(zeile[2]) * -1
                verfahrzeit = float(zeile[3])
                v_pps = (16 * 10 ** 6 * velocity * -1) / (2 ** self.steuerung.getAxisParameter(154, achse)
                                                          * 2048 * (2 ** self.steuerung.getAxisParameter(140, achse)))
                aktuelle_pos = self.steuerung.getAxisParameter(1, achse)
                max_verfahrzeit = int(aktuelle_pos / v_pps) - 1
                if max_verfahrzeit > verfahrzeit:
                    self.steuerung.rotate(motor=achse, velocity=velocity)
                    time.sleep(verfahrzeit)
                    self.steuerung.stop(achse)
                    self.setze_achsparameter()
                else:
                    print("Verfahrzeit zu groß!")
            case "MST":
                achse = int(zeile[1])
                print("Motor stoppt!")
                self.steuerung.stop(achse)
            case "SAP":
                ap_type = int(zeile[1])
                achse = int(zeile[2])
                value = int(zeile[3])
                print(f"Setze Achsenparameter {ap_type}, auf den Wert {value}!")
                self.steuerung.setAxisParameter(ap_type, achse, value)
            case "GAP":
                ap_type = int(zeile[1])
                achse = int(zeile[2])
                value = self.steuerung.getAxisParameter(ap_type, achse)
                print(f"Achsenparameter {ap_type} hat den Wert {value}!")
            case "SIO":
                print("Setze digitalen Output!")
            case "GIO":
                print("Lese digitalen Input!")

    def verfahrgrenze_ueberpruefen(self, zeile, grenze):
        """
        Überprüfe ob Verfahrbewegungen möglich sind, abhängig ob, die
         Verfahrbewegung absolut, relativ oder per Koordinateneingabe geschieht
        :param zeile: Übergabe Befehl
        :param grenze: Verfahrgrenze
        :return: bool
        """
        typ = zeile[1]
        achse = int(zeile[2])
        weg = int(zeile[3])
        if typ == "ABS":
            if 0 <= weg <= int(grenze):
                return True
            else:
                messagebox.showerror(message="Absolutwert zu groß!")
                return False
        elif typ == "REL":
            # akt. pos abfragen und max. Verfahrweg in + und - Richtung ausrechnen
            aktuelle_pos = self.steuerung.getAxisParameter(1, achse)
            max_pos_weg = int(grenze) - aktuelle_pos
            max_neg_weg = aktuelle_pos * -1
            if max_pos_weg > weg > max_neg_weg:
                return True
            else:
                messagebox.showerror(message="Inkrementaler Verfahrweg zu groß!")
                return False

    def messdaten_updaten(self):
        messwerte = [
            self.index,
            time.perf_counter(),
            self.pps_in_mm(0, self.steuerung.getAxisParameter(1, 0)),
            self.pps_in_mm(1, self.steuerung.getAxisParameter(1, 1)),
            self.pps_in_mm(2, self.steuerung.getAxisParameter(1, 2)),
            round(self.cebo.messwert_auslesen() * 1000, 6)
        ]
        self.messdaten.append(messwerte)
        self.index += 1

    @staticmethod
    def messdaten_schreiben(mes_daten):
        """ Schreiben der Messdaten in eine .csv Datei
            Parameter: Index / Zeit / Pos x, y / Value
        """
        header = ["Index", "Zeit in s", "Pos x in mm", "Pos y in mm", "Pos z in mm", "Value in mV"]
        answer = simpledialog.askstring("Input", "Bitte Namen der Messdatei eingeben.")
        # answer is None if user clicks Cancel
        if answer is not None:
            with open(answer, "w", encoding="UTF8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(mes_daten)
