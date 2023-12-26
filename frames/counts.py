#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from calendarium import Calendarium


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="counts")

        self.attributes("-topmost", True)
        self.transient(parent)
        self.resizable(0, 0)
        self.parent = parent
        self.nametowidget(".").engine.center_me(self)
        self.init_ui()

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        self.export_date = Calendarium(frm_left, "Export From")
        self.export_date.get_calendarium(frm_left, 0, 0)

        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)
        
        r = 0
        c = 0
        btn_save = ttk.Button(frm_buttons, style="App.TButton", text="Export", underline=0, command=self.on_export,)
        self.bind("<Alt-e>", self.on_export)
        btn_save.grid(row=r, column=c, sticky=tk.EW, **paddings)
  
        r += 1
        btn_cancel = ttk.Button(frm_buttons, style="App.TButton", text="Cancel", underline=0, command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn_cancel.grid(row=r, column=c, sticky=tk.EW, **paddings)

    def on_open(self):

        self.export_date.set_today()

        self.title("Export Counts")


    def on_export(self, evt=None):

        if self.export_date.get_date(self) == False: return
        if messagebox.askyesno(self.nametowidget(".").title(), "Export data?", parent=self) == True:

            args = (self.export_date.get_date(self),)
            self.nametowidget(".").engine.get_counts(args)
            self.on_cancel()

    def on_cancel(self, evt=None):
        self.destroy()
