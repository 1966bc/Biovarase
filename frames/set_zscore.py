# -*- coding: utf-8 -*-
""" This is the set set_zscore module of Biovarase."""
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2021-03-14"
__status__ = "Production"


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="set_zscore")

        self.parent = parent
        self.attributes('-topmost', True)
        self.transient(parent)
        self.resizable(0, 0)
        
        self.z_score = tk.DoubleVar()
        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)
        self.nametowidget(".").engine.center_me(self)
        self.init_ui()


    def init_ui(self):

        f0 = self.nametowidget(".").engine.get_frame(self, 8)

        w = tk.LabelFrame(f0, text='Set Z Score', font='Helvetica 10 bold')

        self.txValue = ttk.Entry(w, width=8,
                                 justify=tk.CENTER,
                                 textvariable=self.z_score,
                                 validate='key',
                                 validatecommand=self.vcmd)
        self.txValue.pack()

        w.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        bts = [('Save', self.on_save),
               ('Close', self.on_cancel)]

        for btn in bts:
            self.nametowidget(".").engine.get_button(f0, btn[0]).bind("<Button-1>", btn[1])

        self.bind("<Alt-s>", self.on_save)
        self.bind("<Alt-c>", self.on_cancel)

        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self):

        self.z_score.set(self.nametowidget(".").engine.get_zscore())
        self.txValue.focus()
        self.title("Set Z Score")
        
    def on_save(self, evt=None):

        try:

            if self.z_score.get():

                if messagebox.askyesno(self.nametowidget(".").title(),
                                       self.nametowidget(".").engine.ask_to_save,
                                       parent=self) == True:

                    self.nametowidget(".").engine.set_zscore(self.z_score.get())
                    self.parent.set_zscore()
                    self.on_cancel()
        except:
            msg = "Attention\n{0}\nPerhaps the text field is empty?".format(sys.exc_info()[1], sys.exc_info()[0],)

            messagebox.showwarning(self.master.title(), msg, parent=self)                

    def on_cancel(self, evt=None):
        self.destroy()
