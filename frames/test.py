# -*- coding: utf-8 -*-
""" This is the test module of Biovarase."""
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
    def __init__(self, parent, index=None):
        super().__init__(name="test")

        self.parent = parent
        self.index = index
        self.attributes("-topmost", True)
        self.transient(parent)
        self.resizable(0, 0)
        
        self.test = tk.StringVar()
        self.cvw = tk.DoubleVar()
        self.cvb = tk.DoubleVar()
        self.enable = tk.BooleanVar()
        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)

        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        w = self.nametowidget(".").engine.get_init_ui(self)

        r = 0
        ttk.Label(w, text="Samples:").grid(row=r, sticky=tk.W)
        self.cbSamples = ttk.Combobox(w)
        self.cbSamples.grid(row=0, column=1, sticky=tk.W)

        r += 1
        ttk.Label(w, text="Units:").grid(row=r, sticky=tk.W)
        self.cbUnits = ttk.Combobox(w)
        self.cbUnits.grid(row=r, column=1, sticky=tk.W)

        r += 1
        ttk.Label(w, text="Test:").grid(row=r, sticky=tk.W)
        self.txTest = ttk.Entry(w, textvariable=self.test)
        self.txTest.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Cvw:").grid(row=r, sticky=tk.W)
        self.txtCVW = ttk.Entry(w,
                                width=8,
                                justify=tk.CENTER,
                                validate='key',
                                validatecommand=self.vcmd,
                                textvariable=self.cvw)
        self.txtCVW.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Cvb:").grid(row=r, sticky=tk.W)
        self.txtCVB = ttk.Entry(w,
                                width=8,
                                justify=tk.CENTER,
                                validate='key',
                                validatecommand=self.vcmd,
                                textvariable=self.cvb)
        self.txtCVB.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.enable)
        chk.grid(row=r, column=1, sticky=tk.W)

        self.nametowidget(".").engine.get_save_cancel(self, w)


    def on_open(self, selected_item=None):

        self.set_samples()
        self.set_units()

        if self.index is not None:
            self.selected_item = selected_item
            what = "Edit {0}"
            self.set_values()
        else:
            what = "Add {0}"
            self.enable.set(1)
            
        msg = what.format(self.winfo_name().title())
        self.title(msg)
        self.txTest.focus()

    def set_samples(self):

        index = 0
        values = []
        self.dict_samples = {}

        sql = "SELECT sample_id, description FROM samples ORDER BY description ASC"
        rs = self.nametowidget(".").engine.read(True, sql, ())

        for i in rs:
            self.dict_samples[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbSamples['values'] = values


    def set_units(self):

        index = 0
        values = []
        self.dict_units = {}

        sql = "SELECT unit_id, unit FROM units ORDER BY unit ASC"
        rs = self.nametowidget(".").engine.read(True, sql, ())

        for i in rs:
            self.dict_units[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbUnits['values'] = values

    def get_values(self,):

        return [self.dict_samples[self.cbSamples.current()],
                self.dict_units[self.cbUnits.current()],
                self.test.get(),
                self.cvw.get(),
                self.cvb.get(),
                self.enable.get(),]

    def set_values(self,):

        key = next(key for key,
                   value in self.dict_samples.items()
                   if value == self.selected_item[1])
        self.cbSamples.current(key)

        key = next(key for key,
                   value in self.dict_units.items()
                   if value == self.selected_item[2])
        self.cbUnits.current(key)

        self.test.set(self.selected_item[3])
        self.cvw.set(self.selected_item[4])
        self.cvb.set(self.selected_item[5])
        self.enable.set(self.selected_item[6])        

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.field)

                args.append(self.selected_item[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
            self.parent.on_open()

            if self.index is not None:
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)
            else:
                #force focus on listbox
                idx = list(self.parent.dict_items.keys())[list(self.parent.dict_items.values()).index(last_id)]
                self.parent.lstItems.selection_set(idx)
                self.parent.lstItems.see(idx)                 

            self.on_cancel()

            
    def on_cancel(self, evt=None):
        self.destroy()

