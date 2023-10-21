#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="license")

        self.parent = parent
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame", relief=tk.GROOVE, padding=8)
        
        self.txLicense = ScrolledText(frm_left,
                                      wrap = tk.WORD,
                                      bg='light yellow',
                                      relief=tk.GROOVE,
                                      height=height,
                                      width=width,
                                      font='TkFixedFont',)

        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)

    def on_open(self):

        msg = self.nametowidget(".").engine.get_license()

        if msg:
            self.txLicense.insert("1.0", msg)

        self.title(self.nametowidget(".").title())
