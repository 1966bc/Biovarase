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
        super().__init__(name='counts')

        self.parent = parent
        self.attributes('-topmost', True)
        self.resizable(0, 0)
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        w = self.nametowidget(".").engine.get_init_ui(self)

        self.export_date = Calendarium(self, "Export From")
        self.export_date.get_calendarium(w, 0, 0)

        self.nametowidget(".").engine.get_export_cancel(self, self)

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
