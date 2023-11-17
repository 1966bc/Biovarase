#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn 2019
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name='analytical_goals')

        self.resizable(0, 0)
        self.parent = parent
        self.elements = tk.IntVar()
        self.vcmd = self.nametowidget(".").engine.get_validate_integer(self)
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")

        frm_left = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        ttk.Label(frm_left, text='Set elements', style="Data.TLabel").pack()

        self.txElements = ttk.Entry(frm_left, width=8, justify=tk.CENTER,
                                    textvariable=self.elements,
                                    validate='key',
                                    validatecommand=self.vcmd)
        self.txElements.pack()

        frm_buttons = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        bts = (("Export", 0, self.on_export, "<Alt-e>"),
               ("Cancel", 0, self.on_cancel, "<Alt-c>"))

        for btn in bts:
            ttk.Button(frm_buttons,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])

        frm_buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)



    def on_open(self):

        self.title("Analytical Goals")
        self.elements.set(self.nametowidget(".").engine.get_observations())
        self.txElements.focus()

    def on_export(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self, self.nametowidget(".").title()) == False: return


        sql = "SELECT batches.batch_id,\
                      samples.sample,\
                      tests.test,\
                      batches.lot_number,\
                      batches.expiration,\
                      batches.target,\
                      goals.cvw,\
                      goals.cvb,\
                      goals.imp,\
                      goals.bias,\
                      goals.teap005,\
                      goals.teap001,\
                      results.workstation_id\
               FROM tests\
               INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
               INNER JOIN goals ON tests_methods.test_method_id = goals.test_method_id\
               INNER JOIN samples ON tests_methods.sample_id = samples.sample_id\
               INNER JOIN batches ON tests_methods.test_method_id = batches.test_method_id\
               INNER JOIN results ON batches.batch_id = results.batch_id\
               INNER JOIN sections ON tests_methods.section_id = sections.section_id\
               INNER JOIN wards ON sections.ward_id = wards.ward_id\
               INNER JOIN sites ON wards.site_id = sites.site_id\
               INNER JOIN workstations ON results.workstation_id = workstations.workstation_id\
               WHERE tests.status = 1\
               AND sections.section_id =?\
               AND goals.to_export = 1\
               AND batches.status = 1\
               AND batches.expiration IS NOT NULL\
               AND results.is_delete=0\
               AND results.status=1\
               GROUP BY batches.batch_id,results.workstation_id\
               ORDER BY tests.test"
        
        limit = int(self.elements.get())
        rs = self.nametowidget(".").engine.read(True, sql, (self.nametowidget(".").engine.get_section_id(),))

        if rs:
            self.nametowidget(".").engine.get_analitical_goals(limit, rs)
            self.on_cancel()
        else:
            msg = "No record data to compute."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

    def on_cancel(self, evt=None):
        self.destroy()
