# Steuerung_CNC_OOP
Anwendung für Windows um eine CNC-Maschine mit Hilfe eines GUI's zu steuern.
Die Anwendung ist auf den Motion-Controller TMCM-6110 der Firma Trinamic zugeschnitten.
Messdaten werden mit dem CEBO-LC der Firma CESYS ausgelesen.

Features:
- Ansteuerung von 3-Achsen mit unterschiedlicher Geschwindigkeitswahl
- Ausführen von eigens erstellten Skripten im Automatischen- sowie im Einzelschrittmodus
- Hilfestellung für den Skripteditor
- Aufbau der Verbindung zwischen den Systemteilnehmern
- Aufnahme, Speichern, Plotten von Messergebnissen eines Sensors
- Anpassung an unterschiedlichen Maschinen mittels einer config.ini Datei

# Installieren der benötigten Module
Das Repository enthält eine Textdatei namens requirements.txt, diese enthält alle benötigten Module.
Der Befehl zum Installieren dieser Module lautet:
- pip install -r <requirements.txt>

