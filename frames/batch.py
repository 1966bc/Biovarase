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
__date__ = "2019-10-18"
__status__ = "Production"

class UI(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='batch')

        self.attributes('-topmost', True)
        self.transient(parent)
        self.resizable(0, 0)

        self.parent = parent
        self.engine = kwargs['engine']
        self.index = kwargs['index']

        self.batch = tk.StringVar()
        self.target = tk.DoubleVar()
        self.sd = tk.DoubleVar()
        self.enable = tk.BooleanVar()

        self.vcmd = self.engine.get_validate_float(self)
        self.engine.center_me(self)
        self.init_ui()


    def init_ui(self):

        w = self.engine.get_init_ui(self)

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

        self.engine.get_save_cancel(self, w)


    def on_open(self, selected_test, selected_batch=None):

        self.selected_test = selected_test

        if self.index is not None:
            self.selected_batch = selected_batch
            msg = "{0} {1}".format("Update ", self.selected_batch[2])
            self.set_values()
        else:
            msg = "{0} {1}".format("Insert new batch for ", selected_test[1])
            self.expiration_date.set_today()
            self.target.set('')
            self.sd.set('')
            self.enable.set(1)

        self.title(msg)
        self.txtBatch.focus()


    def on_save(self, evt=None):

        if self.engine.on_fields_control(self) == False: return
        if self.expiration_date.get_date(self) == False: return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.engine.get_update_sql('batches', 'batch_id')

                args = (*args, self.selected_batch[0])

            else:

                sql = self.engine.get_insert_sql('batches', len(args))

            self.engine.write(sql, args)


            if self.index is not None:
                if self.parent.winfo_name() == 'data':
                    self.parent.set_batches()
                    self.parent.lstBatches.focus(self.index)
                    self.parent.lstBatches.selection_set(self.index)

                else:
                    self.parent.lstBatches.see(self.index)
                    self.parent.lstBatches.selection_set(self.index)
                    self.parent.lstBatches.event_generate("<<ListboxSelect>>")

            self.on_cancel()

        else:
            messagebox.showinfo(self.engine.title, self.engine.abort, parent=self)


    def get_values(self,):

        return (self.selected_test[0],
                self.batch.get(),
                self.expiration_date.get_date(self),
                self.target.get(),
                self.sd.get(),
                self.enable.get())


    def set_values(self,):

        self.expiration_date.year.set(int(self.selected_batch[3][0:4]))
        self.expiration_date.month.set(int(self.selected_batch[3][5:7]))
        self.expiration_date.day.set(int(self.selected_batch[3][8:10]))
        self.batch.set(self.selected_batch[2])
        self.target.set(self.selected_batch[4])
        self.sd.set(self.selected_batch[5])
        self.enable.set(self.selected_batch[6])

    def on_cancel(self, evt=None):
        self.destroy()
