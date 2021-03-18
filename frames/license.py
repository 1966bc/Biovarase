# -*- coding: utf-8 -*-
""" This is the license module of Biovarase."""
import tkinter as tk
from tkinter import ttk

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
        super().__init__(name="license")

        self.parent = parent
        #self.resizable(0, 0)
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        w = ttk.Frame(self, padding=4)

        self.txLicense = self.nametowidget(".").engine.get_text_box(w,)

        w.pack(fill=tk.BOTH, expand=1)


    def on_open(self):

        msg = self.nametowidget(".").engine.get_license()

        if msg:
            self.txLicense.insert("1.0", msg)

        self.title(self.master.title())

