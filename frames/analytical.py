#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn 2019
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="analitical")

        self.parent = parent
        self.attributes('-topmost', True)
        self.transient(parent) 
        self.resizable(0, 0)
        self.nametowidget(".").engine.center_me(self)
        self.init_ui()

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)


        items = (("k CV:", self.nametowidget(".").engine.get_rgb(240, 240, 237)), ("0.25", "green"), ("0.50", "yellow"), ("0.75", "red"),)

        r = 0
        c = 0
        for i in items:
            tk.Label(frm_left, bg=i[1], text=i[0]).grid(row=r, column=c, sticky=tk.W, padx=10, pady=10)
            r += 1


        items = (("k Bias:", self.nametowidget(".").engine.get_rgb(240, 240, 237),), ("0.125<= k <= 0.25", "green"),
                 ("0.25<= k <= 0.375", "yellow"), ("k > 0.375", "red"),)

        r = 0
        c = 1
        for i in items:
            tk.Label(frm_left, bg=i[1], text=i[0]).grid(row=r, column=c, sticky=tk.W, padx=10, pady=10)
            r += 1

        items = (("Eta:", self.nametowidget(".").engine.get_rgb(240, 240, 237)),
                 ("ETa < 1.65 (0.25 CVi) + 0.125 (CVi2+ CVg2) ½ ", "green"),
                 ("ETa < 1.65 (0.50 CVi) + 0.25 (CVi2 + CVg2) ½", "yellow"), 
                 ("ETa < 1.65 (0.75 CVi) + 0.375 (CVi2+ CVg2) ½", "red"),)

        r = 0
        c = 2
        for i in items:
            tk.Label(frm_left, bg=i[1], text=i[0]).grid(row=r, column=c, sticky=tk.W, padx=10, pady=10)
            r += 1


    def on_open(self,):

        self.title("Analytical Goals Explained")


    def on_cancel(self, evt=None):
        self.destroy()
