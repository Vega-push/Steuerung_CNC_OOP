import tkinter as tk
import tkinter.scrolledtext


class Gui(tk.Tk):

    FONT = ("Impact", 20, "normal")

    def __init__(self):
        super().__init__()
        self.title("CNC-Steuerung")
        self.config(padx=50, pady=50)

        # create widgets
        self.btn_ref = tk.Button(bd=5, font=self.FONT, text="Referenzfahrt")
        self.btn_auto = tk.Button(bd=5, font=self.FONT, text="Automatik Modus", command=self.auto_window)
        self.btn_clear_infobox = tk.Button(bd=5, font=self.FONT, text="Clear")
        self.mainframe = tk.LabelFrame(text="Manuelle Steuerung", labelanchor="n")
        self.tf_infobox = tk.scrolledtext.ScrolledText(width=80, height=5, state="normal")

        self.axis = tk.IntVar(master=self, value=2)
        self.btn_y = tk.Radiobutton(master=self.mainframe, text='Y-Achse', variable=self.axis, value=0)
        self.btn_x = tk.Radiobutton(master=self.mainframe, text='X-Achse', variable=self.axis, value=1)
        self.btn_z = tk.Radiobutton(master=self.mainframe, text='Z-Achse', variable=self.axis, value=2)

        self.geschwindigkeit = tk.IntVar(master=self, value=1000)
        self.btn_01 = tk.Radiobutton(master=self.mainframe, text='500pps', variable=self.geschwindigkeit, value=500)
        self.btn_1 = tk.Radiobutton(master=self.mainframe, text='1000pps', variable=self.geschwindigkeit, value=1000)
        self.btn_10 = tk.Radiobutton(master=self.mainframe, text='1500pps', variable=self.geschwindigkeit, value=1500)

        self.btn_plus = tk.Button(master=self.mainframe, bd=3, font=self.FONT, text=" + ")
        self.btn_minus = tk.Button(master=self.mainframe, bd=3, font=self.FONT, text=" - ")

        self.btn_plus.bind('<ButtonPress-1>', lambda event: 0)
        self.btn_plus.bind('<ButtonRelease-1>', lambda event: 0)
        self.btn_minus.bind('<ButtonPress-1>', lambda event: 0)
        self.btn_minus.bind('<ButtonRelease-1>', lambda event: 0)

        self.btn_ref.grid(column=0, row=0)
        self.btn_auto.grid(column=1, row=0)

        self.mainframe.grid(column=0, columnspan=2, row=1)
        self.btn_x.grid(column=0, columnspan=2, row=0)
        self.btn_y.grid(column=2, columnspan=2, row=0)
        self.btn_z.grid(column=4, columnspan=2, row=0)
        self.btn_01.grid(column=0, columnspan=2, row=1)
        self.btn_1.grid(column=2, columnspan=2, row=1)
        self.btn_10.grid(column=4, columnspan=2, row=1)
        self.btn_plus.grid(column=0, columnspan=3, row=2)
        self.btn_minus.grid(column=3, columnspan=3, row=2)

        self.tf_infobox.grid(column=0, columnspan=2, row=2)
        self.btn_clear_infobox.grid(column=0, columnspan=2, row=3)

        self.mainloop()

    def auto_window(self):
        auto_window = tk.Toplevel(self)
        auto_window.title("Automatischer Modus")

        self.auto_textbox = tk.Text(master=auto_window, width=40, height=40)
        self.btn_start = tk.Button(master=auto_window, bd=5, font=self.FONT, text="Start")
        self.btn_load = tk.Button(master=auto_window, bd=5, font=self.FONT, text="Speichern")
        self.btn_save = tk.Button(master=auto_window, bd=5, font=self.FONT, text="Laden")

        self.auto_textbox.grid(column=0, columnspan=3, row=0)
        self.btn_start.grid(column=0, row=1)
        self.btn_save.grid(column=1, row=1)
        self.btn_load.grid(column=2, row=1)
