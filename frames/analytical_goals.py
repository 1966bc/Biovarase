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
__date__ = "2019-05-02"
__status__ = "Production"


class Widget(tk.Toplevel):     
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='analytical_goals')  

        self.resizable(0,0)
        self.parent = parent
        self.engine = kwargs['engine']
        self.elements = tk.IntVar()
        self.vcmd = self.engine.get_validate_integer(self)
        self.init_ui()
        self.engine.center_me(self)

    def init_ui(self):

        f0 = self.engine.get_frame(self, 8)
        
        w = tk.LabelFrame(f0,text='Set elements to export', font='Helvetica 10 bold')

        self.txElements = ttk.Entry(w, width=8, justify=tk.CENTER,
                                    textvariable=self.elements,
                                    validate = 'key',
                                    validatecommand = self.vcmd)
        self.txElements.pack()

        w.pack(side=tk.LEFT, fill=tk.BOTH,padx=5, pady=5, expand =1)

        bts = [('Export', self.on_save),
               ('Close', self.on_cancel)]

        for btn in bts:
            self.engine.get_button(f0, btn[0] ).bind("<Button-1>", btn[1])

        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self):

        self.title("Analytical Goals")
        self.elements.set(self.engine.get_elements())
        self.txElements.focus()
        
        
    def on_save(self, evt=None):

        
        if self.engine.on_fields_control(self)==False:return

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
        rs = self.engine.read(True, sql, ())

        if rs:
            self.engine.get_analitical_goals(limit,rs)
            self.on_cancel()
        else:
            msg = "No record data to compute analytical goals."
            messagebox.showwarning(self.engine.title, msg, parent=self)

    def on_cancel(self, evt=None):
        self.destroy()
