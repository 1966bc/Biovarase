# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="zscore")

        self.parent = parent
        self.attributes('-topmost', True)
        self.transient(parent) 
        self.resizable(0,0)
        self.nametowidget(".").engine.center_me(self)
        self.init_ui()

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        ttk.Label(frm_left, text="Z-Score").grid(row=0, sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left, text="2.33").grid(row=1,column=0,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left, text="2.05").grid(row=2,column=0,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left, text="1.88").grid(row=3,column=0,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left, text="1.75").grid(row=4,column=0,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left, text="1.65").grid(row=5,column=0,sticky=tk.W,padx=10,pady=10)

        ttk.Label(frm_left,text="P Value").grid(row=0,column=1, sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="p>0.01").grid(row=1,column=1,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="p>0.02").grid(row=2,column=1,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="p>0.03").grid(row=3,column=1,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="p>0.04").grid(row=4,column=1,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="p>0.05").grid(row=5,column=1,sticky=tk.W,padx=10,pady=10)

        ttk.Label(frm_left, text="Probability").grid(row=0,column=2, sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="99%").grid(row=1,column=2,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="98%").grid(row=2,column=2,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="97%").grid(row=3,column=2,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="96%").grid(row=4,column=2,sticky=tk.W,padx=10,pady=10)
        ttk.Label(frm_left,text="95%").grid(row=5,column=2,sticky=tk.W,padx=10,pady=10)

    def on_open(self,):

        self.title("Probability")
        
    def on_cancel(self, evt=None):
        self.destroy()
