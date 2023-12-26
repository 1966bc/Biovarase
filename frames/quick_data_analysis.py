# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from calendarium import Calendarium

class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="quick_data_analysis")

        self.parent = parent
        self.attributes('-topmost', True)
        self.transient(parent)
        self.resizable(0, 0)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        self.analysis_date = Calendarium(self, "Set a date:")
        self.analysis_date.get_calendarium(frm_left, r, c)

        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)
        
        r = 0
        c = 0
        btn_save = ttk.Button(frm_buttons, style="App.TButton", text="Export", underline=0, command=self.on_export,)
        self.bind("<Alt-e>", self.on_export)
        btn_save.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        btn = ttk.Button(frm_buttons, style="App.TButton", text="Cancel", underline=0, command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

    def on_open(self):

        self.analysis_date.set_today()
        self.title("Quick Data Analysis")

    def on_export(self, evt=None):

        if self.analysis_date.get_date(self) == False: return

        args = (self.analysis_date.get_date(self),)
        self.nametowidget(".").engine.quick_data_analysis(args)
        self.on_cancel()

    def on_cancel(self, evt=None):
        self.destroy()
