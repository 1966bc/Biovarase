# -*- coding: utf-8 -*-
""" This is the analitical_goals module of Biovarase."""
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
        super().__init__(name='analytical_goals')

        self.parent = parent
        self.attributes('-topmost', True)
        self.resizable(0, 0)
        self.elements = tk.IntVar()
        self.vcmd = self.nametowidget(".").engine.get_validate_integer(self)
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)


    def init_ui(self):

        w = self.nametowidget(".").engine.get_frame(self, 8)

        f = tk.LabelFrame(w, text='Set elements to export', font='Helvetica 10 bold')

        self.txElements = ttk.Entry(f, width=8, justify=tk.CENTER,
                                    textvariable=self.elements,
                                    validate='key',
                                    validatecommand=self.vcmd)
        self.txElements.pack()

        f.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        bts = [('Export', self.on_export), ('Close', self.on_cancel)]

        for btn in bts:
            self.nametowidget(".").engine.get_button(w, btn[0]).bind("<Button-1>", btn[1])

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


    def on_open(self):

        self.title("Analytical Goals")
        self.elements.set(self.nametowidget(".").engine.get_elements())
        self.txElements.focus()

    def on_export(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self) == False: return

        sql = "SELECT batches.batch_id,\
                         samples.sample,\
                      tests.test,\
                      batches.batch,\
                      batches.expiration,\
                      batches.target,\
                      tests.cvw,\
                      tests.cvb\
               FROM tests\
               INNER JOIN samples \
               ON tests.sample_id = samples.sample_id\
               INNER JOIN batches \
               ON tests.test_id = batches.test_id\
               WHERE tests.enable = 1\
               AND tests.cvw !=0\
               AND tests.cvb !=0\
               AND batches.target !=0\
               AND batches.enable = 1\
               ORDER BY tests.test,samples.sample"

        limit = int(self.elements.get())
        rs = self.nametowidget(".").engine.read(True, sql, ())

        if rs:
            self.nametowidget(".").engine.get_analitical_goals(limit, rs)
            self.on_cancel()
        else:
            msg = "No record data to compute analytical goals."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

    def on_cancel(self, evt=None):
        self.destroy()
