import tkinter
from tkinter import Tk
import tkinter.scrolledtext


class Gui(Tk):

    def __init__(self, maschine):
        self.window = Tk()
        self.window.title("Steuerung CNC")
        tkinter.mainloop()


# def erstelle_main_window(maschine):
#     ####################
#     # Funktionen Buttons
#     ####################
#     def clear_infobox():
#         tf_infobox.delete(1.0, "end")
#
#
#     # def auto_window():
#         # erstelle_auto_window(master, steuerung, antriebsstrang)
#
#     ###################
#     # Widgets erstellen
#     ###################
#     btn_ref = tk.Button(master, bd=3, font="Arial", text="Referenzfahrt", width=30, height=1, command=lambda: controls.np_referenzfahrt(steuerung, antriebsstrang, tf_infobox))
#     btn_auto = tk.Button(master, bd=3, font="Arial", text="Automatik Modus", width=30, height=1, command=auto_window)
#     btn_clear_infobox = tk.Button(master, bd=3, font="Arial", text="Clear", width=20, height=1, command=clear_infobox)
#     mainframe = tk.LabelFrame(master, text="Manuelle Steuerung", labelanchor="n")
#     tf_infobox = tk.scrolledtext.ScrolledText(master, width=80, height=5, state="normal")
#     # Achsenauswahl erstellen
#     axis = tk.IntVar(mainframe, 2)
#     btn_x = tk.Radiobutton(mainframe, text='X-Achse', variable=axis, value=1, width=30, height=2)
#     btn_y = tk.Radiobutton(mainframe, text='Y-Achse', variable=axis, value=0, width=30, height=2)
#     btn_z = tk.Radiobutton(mainframe, text='Z-Achse', variable=axis, value=2, width=30, height=2)
#     # Geschwindigkeitsauswahl erstellen
#     geschwindigkeit = tk.IntVar(mainframe, value=1000)
#     btn_01 = tk.Radiobutton(mainframe, text='500pps', variable=geschwindigkeit, value=500)
#     btn_1 = tk.Radiobutton(mainframe, text='1000pps', variable=geschwindigkeit, value=1000)
#     btn_10 = tk.Radiobutton(mainframe, text='1500pps', variable=geschwindigkeit, value=1500)
#     # Richtungs-Buttons erstellen main_window
#     btn_plus = tk.Button(mainframe, bd=3, font="Arial", text=" + ", width=10, height=2)
#     btn_minus = tk.Button(mainframe, bd=3, font="Arial", text=" - ", width=10, height=2)
#     # gedrückt halten zum Fahren/loslassen zum Stoppen
#     btn_plus.bind('<ButtonPress-1>', lambda event: controls.manual_mode(steuerung, axis, "+", geschwindigkeit))
#     btn_plus.bind('<ButtonRelease-1>', lambda event: controls.stop_manual_mode(steuerung, axis, tf_infobox, antriebsstrang))
#     btn_minus.bind('<ButtonPress-1>', lambda event: controls.manual_mode(steuerung, axis, "-", geschwindigkeit))
#     btn_minus.bind('<ButtonRelease-1>', lambda event: controls.stop_manual_mode(steuerung, axis, tf_infobox, antriebsstrang))
#
#     ##################
#     # Widgets "packen"
#     ##################
#     btn_ref.grid(column=0, row=0, padx=30, pady=15)
#     btn_auto.grid(column=1, row=0, padx=30, pady=15)
#     #### frame ####
#     mainframe.grid(column=0, columnspan=2, row=1, padx=30, pady=15)
#     btn_x.grid(column=0, columnspan=2, row=0)
#     btn_y.grid(column=2, columnspan=2, row=0)
#     btn_z.grid(column=4, columnspan=2, row=0)
#     btn_01.grid(column=0, columnspan=2, row=1)
#     btn_1.grid(column=2, columnspan=2, row=1)
#     btn_10.grid(column=4, columnspan=2, row=1)
#     btn_plus.grid(column=0, columnspan=3, row=2, padx=30, pady=15)
#     btn_minus.grid(column=3, columnspan=3, row=2, padx=30, pady=15)
#     ##############
#     tf_infobox.grid(column=0, columnspan=2, row=2, padx=30, pady=15)
#     btn_clear_infobox.grid(column=0, columnspan=2, row=3, padx=30, pady=5)
