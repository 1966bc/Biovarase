# -*- coding: utf-8 -*-
""" This is the export_rejections module of Biovarase."""
import tkinter as tk
from tkinter import messagebox
from calendarium import Calendarium

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
        super().__init__(name='export_rejection')

        self.parent = parent
        self.resizable(0, 0)
        self.transient(parent)

        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        w = self.nametowidget(".").engine.get_init_ui(self)

        r = 0
        self.start_date = Calendarium(self, "Start Date")
        self.start_date.get_calendarium(w, r)

        self.nametowidget(".").engine.get_export_cancel(self, w)

    def on_open(self):

        self.start_date.set_today()

        self.title("Export Rejections Data")

    def on_export(self, evt=None):

        if self.start_date.get_date(self) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(), "Export data?", parent=self) == True:
            args = (self.start_date.get_date(self),)
            self.nametowidget(".").engine.get_rejections(args)
            self.on_cancel()

    def on_cancel(self, evt=None):
        self.destroy()
