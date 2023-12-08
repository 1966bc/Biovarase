# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="set_zscore")

        self.parent = parent
        self.attributes('-topmost', True)
        self.transient(parent) 
        self.resizable(0,0)
        
        self.z_score = tk.DoubleVar()
        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)


    def init_ui(self):

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)

        w = tk.LabelFrame(self.frm_main, text="Set", font="Helvetica 10 bold", bg=self.nametowidget(".").engine.get_rgb(240, 240, 237))

        self.txValue = ttk.Entry(w,
                                 width=8,
                                 justify=tk.CENTER,
                                 validate="key",
                                 validatecommand=self.vcmd,
                                 textvariable=self.z_score,)
        self.txValue.pack()

        w.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        frm_bts = ttk.Frame(self.frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)


        bts = (("Save", 0, self.on_save, "<Alt-s>"),
               ("Cancel", 0, self.on_cancel, "<Alt-c>"))

        for btn in bts:
            ttk.Button(frm_bts,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])

        frm_bts.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        self.frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)

    def on_open(self):

        self.z_score.set(self.nametowidget(".").engine.get_zscore())
        self.title("Set Z Score")
        self.txValue.focus()

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(), self.nametowidget(".").engine.ask_to_save, parent=self) == True:
            #notice, same name callback but different class
            self.nametowidget(".").engine.set_zscore(self.z_score.get())
            self.parent.set_zscore()
            self.on_cancel()

    def on_cancel(self, evt=None):
        self.destroy()
