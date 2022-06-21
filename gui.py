import tkinter as tk
import tkinter.scrolledtext
import tkinter.filedialog
from tkinter import ttk
import time


class Gui(tk.Tk):
    FONT = ("Impact", 20, "normal")

    def __init__(self, *args, **kwargs):
        self.window = super().__init__()
        self.maschine = args[0]
        self.skript = []
        self.title("CNC-Steuerung")
        self.config(padx=50, pady=50)

        # ----------------------------- Register manueller Betrieb ---------------------------------------- #
        # Register
        self.tab_control = ttk.Notebook(self)
        self.tab_man = tk.Frame(self.tab_control)
        self.tab_auto = tk.Frame(self.tab_control)
        self.tab_hilfe = tk.Frame(self.tab_control)
        self.tab_control.add(self.tab_man, text="Manuell")
        self.tab_control.add(self.tab_auto, text="Auto")
        self.tab_control.add(self.tab_hilfe, text="Hilfe")

        # Frame für Radiobuttons
        self.mainframe = tk.LabelFrame(master=self.tab_man, text="Manuelle Steuerung", labelanchor="n", pady=20)

        # Buttons
        self.btn_ref = tk.Button(master=self.tab_man, bd=5, font=self.FONT,
                                 text="Referenzfahrt", command=self.maschine.np_referenzfahrt)
        self.btn_np = tk.Button(master=self.tab_man, bd=5, font=self.FONT,
                                text="NP setzen", command=lambda: self.maschine.setze_resette_np(self.btn_np))
        self.btn_clear_infobox = tk.Button(master=self.tab_man, bd=5, font=self.FONT,
                                           text="Clear", command=self.loesche_infobox)
        self.btn_plus = tk.Button(master=self.mainframe, bd=3, font=self.FONT, text=" + ", width=4)
        self.btn_minus = tk.Button(master=self.mainframe, bd=3, font=self.FONT, text=" - ", width=4)

        # Infobox
        self.tf_infobox = tk.scrolledtext.ScrolledText(master=self.tab_man, width=70, height=5, state="normal", pady=20)

        # Radiobuttons
        self.axis = tk.IntVar(master=self, value=2)
        self.btn_y = tk.Radiobutton(master=self.mainframe, text='Y-Achse', variable=self.axis, value=0, pady=10)
        self.btn_x = tk.Radiobutton(master=self.mainframe, text='X-Achse', variable=self.axis, value=1)
        self.btn_z = tk.Radiobutton(master=self.mainframe, text='Z-Achse', variable=self.axis, value=2)

        self.geschwindigkeit = tk.IntVar(master=self, value=1000)
        self.btn_01 = tk.Radiobutton(master=self.mainframe, text='500pps',
                                     variable=self.geschwindigkeit, value=500, width=23, pady=10)
        self.btn_1 = tk.Radiobutton(master=self.mainframe, text='1000pps',
                                    variable=self.geschwindigkeit, value=1000, width=23)
        self.btn_10 = tk.Radiobutton(master=self.mainframe, text='1500pps',
                                     variable=self.geschwindigkeit, value=1500, width=23)

        self.btn_plus.bind('<ButtonPress-1>',
                           lambda event: self.maschine.manual_mode(self.axis, "+", self.geschwindigkeit))
        self.btn_plus.bind('<ButtonRelease-1>',
                           lambda event: self.maschine.stop_manual_mode(self.axis, self.tf_infobox))
        self.btn_minus.bind('<ButtonPress-1>',
                            lambda event: self.maschine.manual_mode(self.axis, "-", self.geschwindigkeit))
        self.btn_minus.bind('<ButtonRelease-1>',
                            lambda event: self.maschine.stop_manual_mode(self.axis, self.tf_infobox))

        # Platziere Widgets
        self.tab_control.grid(column=0, row=0)
        self.btn_ref.grid(column=0, row=1)
        self.btn_np.grid(column=2, row=1)

        self.mainframe.grid(column=0, columnspan=3, row=2)
        self.btn_x.grid(column=0, columnspan=2, row=0)
        self.btn_y.grid(column=2, columnspan=2, row=0)
        self.btn_z.grid(column=4, columnspan=2, row=0)
        self.btn_01.grid(column=0, columnspan=2, row=1)
        self.btn_1.grid(column=2, columnspan=2, row=1)
        self.btn_10.grid(column=4, columnspan=2, row=1)
        self.btn_plus.grid(column=0, columnspan=3, row=2)
        self.btn_minus.grid(column=3, columnspan=3, row=2)

        self.tf_infobox.grid(column=0, columnspan=3, row=3)
        self.btn_clear_infobox.grid(column=0, columnspan=3, row=4)

        # ----------------------------- Register Automatikbetrieb ---------------------------------------- #
        # Buttons
        self.btn_start = tk.Button(master=self.tab_auto, bd=5, font=self.FONT,
                                   text="Start", command=self.starte_programm)
        self.btn_load = tk.Button(master=self.tab_auto, bd=5, font=self.FONT,
                                  text="Speichern", command=self.skript_speichern)
        self.btn_save = tk.Button(master=self.tab_auto, bd=5, font=self.FONT,
                                  text="Laden", command=self.skript_laden)
        self.single_flag = tk.IntVar()
        self.check_single = tk.Checkbutton(master=self.tab_auto, bd=3, font="Arial",
                                           text="Schrittmodus", variable=self.single_flag)

        # Skriptbox
        self.skriptbox = tk.scrolledtext.ScrolledText(master=self.tab_auto, width=70, height=25, state="normal")

        # Platziere Widgets
        self.skriptbox.grid(column=0, columnspan=4, row=0)
        self.btn_start.grid(column=0, row=1)
        self.btn_save.grid(column=1, row=1)
        self.btn_load.grid(column=2, row=1)
        self.check_single.grid(column=3, row=1)

        # ----------------------------- Register manueller Betrieb ---------------------------------------- #
        self.hilfe_box = tk.scrolledtext.ScrolledText(master=self.tab_hilfe, width=70, height=30, state="normal")
        self.hilfe_box.pack()
        self.hilfe_laden()

    def loesche_infobox(self):
        self.tf_infobox.delete(1.0, "end")

    def hilfe_laden(self):
        with open(file="Befehlsliste.txt", mode="r") as file:
            daten = file.readlines()
            for item in daten:
                self.hilfe_box.insert(tk.END, item)

    def skript_speichern(self):
        """speichert den aktuellen Inhalt des Textfeldes in eine .txt Datei"""
        textfeld_inhalt = self.skriptbox.get(1.0, "end")
        textfeld_inhalt = textfeld_inhalt.strip()
        datei = tk.filedialog.asksaveasfile(mode="w", defaultextension="txt", filetypes=[("Text file", "*.txt")])
        datei.write(textfeld_inhalt)
        datei.close()

    def skript_laden(self):
        """laden einer .txt Datei in das Textfeld"""
        self.skriptbox.delete("1.0", "end")
        datei = tk.filedialog.askopenfile(mode="r", filetypes=[("Text file", "*.txt")])
        if datei:
            self.skriptbox.insert("1.0", datei.read().upper())
            datei.close()

    def starte_programm(self):
        self.maschine.skript_ausfuehren(self.single_flag, self.skriptbox)
