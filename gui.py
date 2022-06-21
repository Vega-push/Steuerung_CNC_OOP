import tkinter as tk
import tkinter.scrolledtext
from tkinter import ttk
import random
import time
from maschine import Maschine


class Gui(tk.Tk):
    FONT = ("Impact", 20, "normal")

    def __init__(self, *args, **kwargs):
        self.window = super().__init__()
        self.skript = []
        self.title("CNC-Steuerung")
        self.config(padx=50, pady=50)
        self.std_np = [0, 0, 0]

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
                                 text="Referenzfahrt", command=Maschine.np_referenzfahrt)
        self.btn_np = tk.Button(master=self.tab_man, bd=5, font=self.FONT,
                                text="NP setzen", command=self.setze_resette_np)
        self.btn_clear_infobox = tk.Button(master=self.tab_man, bd=5, font=self.FONT, text="Clear")
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

        self.btn_plus.bind('<ButtonPress-1>', lambda event: 0)
        self.btn_plus.bind('<ButtonRelease-1>', lambda event: 0)
        self.btn_minus.bind('<ButtonPress-1>', lambda event: 0)
        self.btn_minus.bind('<ButtonRelease-1>', lambda event: 0)

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
                                   text="Start", command=self.highlight_text)
        self.btn_load = tk.Button(master=self.tab_auto, bd=5, font=self.FONT, text="Speichern")
        self.btn_save = tk.Button(master=self.tab_auto, bd=5, font=self.FONT, text="Laden", command=self.skript_laden)
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

    def setze_resette_np(self):
        """
        setze oder resette die NP der Achsen an der aktuellen Position.
        Bevor NP's gesetzt werden, wird die aktuelle Achsposition gepseichert,
        um später die standardmäßigen NP's wiederherstellen zu können.
        """
        if self.btn_np["text"] == "NP setzen":
            # lese aktuelle Werte ein
            self.std_np = [random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)]
            # setze NP hier
            print("x - 0 gesetzt")
            print("y - 0 gesetzt")
            print("z - 0 gesetzt")
            self.btn_np["text"] = "NP resetten"
        elif self.btn_np["text"] == "NP resetten":
            # resette Nullpunkt
            # fahre auf x, y, z = 0 und setze achsposition auf self.xyz-wert
            print("fahre Achsen auf NP's")
            print(f"x - {self.std_np[0]} gesetzt")
            print(f"y - {self.std_np[1]} gesetzt")
            print(f"z - {self.std_np[2]} gesetzt")
            self.btn_np["text"] = "NP setzen"

    def skript_laden(self):
        with open(file="messprogramm.txt", mode="r") as file:
            data = file.readlines()
            self.skript = [item.upper() for item in data]
        print(self.skript)
        for row in self.skript:
            self.skriptbox.insert(tk.END, row)

    def highlight_text(self):
        for i in range(len(self.skript)):
            self.skriptbox.tag_add("start", f"{i + 1}.0", f"{i + 1}.end")
            self.skriptbox.tag_config("start", background="red", foreground="white")
            self.skriptbox.update()
            time.sleep(1)
            self.skriptbox.tag_delete("start")
