# -*- coding: utf-8 -*-
""" This is the batch module of Biovarase."""
import tkinter as tk
from tkinter import ttk
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
    def __init__(self, parent, index=None):
        super().__init__(name="batch")

        self.attributes("-topmost", True)
        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)

        self.batch = tk.StringVar()
        self.target = tk.DoubleVar()
        self.sd = tk.DoubleVar()
        self.enable = tk.BooleanVar()

        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)
        self.nametowidget(".").engine.center_me(self)
        self.init_ui()


    def init_ui(self):

        w = self.nametowidget(".").engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, text="Batch:").grid(row=r, sticky=tk.W)
        self.txtBatch = ttk.Entry(w, textvariable=self.batch)
        self.txtBatch.grid(row=r, column=c, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Expiration:").grid(row=r, sticky=tk.N+tk.W)
        self.expiration_date = Calendarium(self, "")
        self.expiration_date.get_calendarium(w, r, c)


        r += 1
        ttk.Label(w, text="Target:").grid(row=r, sticky=tk.W)
        self.txtTarget = ttk.Entry(w,
                                   width=8,
                                   justify=tk.CENTER,
                                   validate='key',
                                   validatecommand=self.vcmd,
                                   textvariable=self.target)
        self.txtTarget.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="SD:").grid(row=r, sticky=tk.W)
        self.txtSD = ttk.Entry(w,
                               width=8,
                               justify=tk.CENTER,
                               validate='key',
                               validatecommand=self.vcmd,
                               textvariable=self.sd)
        self.txtSD.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.enable)
        chk.grid(row=r, column=c, sticky=tk.W)

        self.nametowidget(".").engine.get_save_cancel(self, w)


    def on_open(self, selected_test, selected_batch=None):

        self.selected_test = selected_test

        if self.index is not None:
            self.selected_batch = selected_batch
            msg = "Update {0} for {1}".format(self.winfo_name(), selected_test[1])
            self.set_values()
        else:
            msg = "Insert {0} for {1}".format(self.winfo_name(), selected_test[1])
            self.expiration_date.set_today()
            self.target.set('')
            self.sd.set('')
            self.enable.set(1)

        self.title(msg)
        self.txtBatch.focus()


    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self) == False: return
        if self.expiration_date.get_date(self) == False: return
        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql('batches', 'batch_id')

                args = (*args, self.selected_batch[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql('batches', len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
            self.parent.set_batches()


            if self.index is not None:
                if self.parent.winfo_name() == "data":
                    self.parent.lstBatches.focus()
                    self.parent.lstBatches.selection_set(self.index)
                    self.nametowidget(".").nametowidget("biovarase").set_batches()

                else:
                    self.parent.lstBatches.see(self.index)
                    self.parent.lstBatches.selection_set(self.index)
                    self.parent.lstBatches.event_generate("<<ListboxSelect>>")
            else:
                self.parent.lstBatches.selection_set(last_id)
                self.parent.lstBatches.see(last_id)

            self.on_cancel()


    def get_values(self,):

        return (self.selected_test[0],
                self.batch.get(),
                self.expiration_date.get_date(self),
                self.target.get(),
                self.sd.get(),
                self.enable.get())


    def set_values(self,):

        self.batch.set(self.selected_batch[2])
        self.expiration_date.year.set(int(self.selected_batch[3][0:4]))
        self.expiration_date.month.set(int(self.selected_batch[3][5:7]))
        self.expiration_date.day.set(int(self.selected_batch[3][8:10]))
        self.target.set(self.selected_batch[4])
        self.sd.set(self.selected_batch[5])
        self.enable.set(self.selected_batch[6])

    def on_cancel(self, evt=None):
        self.destroy()
