# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="load_tests_methods")

        self.attributes("-topmost", True)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.init_ui()
        self.nametowidget(".").engine.center_window_on_screen(self)
        self.nametowidget(".").engine.set_instance(self, 1)

    def init_ui(self):

        w = ttk.Frame(self, style="App.TFrame", padding=8)
        sb = ttk.Scrollbar(w, orient=tk.VERTICAL)
        self.lstItems = tk.Listbox(w, yscrollcommand=sb.set,)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        sb.config(command=self.lstItems.yview)
        self.lstItems.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)
        w.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)

    def on_open(self, selected_workstation, tests_method_assigned):

        self.related_ids = self.nametowidget(".").engine.get_related_ids_by_section(selected_workstation[5])

        comp_id = self.related_ids[2]

        self.selected_workstation = selected_workstation
        self.tests_method_assigned = tests_method_assigned
        args = (selected_workstation[0],)
        self.set_values(tests_method_assigned)

        sql = "SELECT sites.site_id, suppliers.description AS site\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id\
               WHERE sites.comp_id =?;"
        
        args = (comp_id,)
        rs = self.nametowidget(".").engine.read(False, sql, args)
        msg = "{0} assign test method".format(rs[1])
        self.title(msg)

    def set_values(self, args):

        self.lstItems.delete(0, tk.END)

        if len(args) != 0:

            s = (",".join(["?"]*len(args)))

            sql = "SELECT dict_tests.dict_test_id,\
                        tests.description || ' ' || samples.sample,\
                        labs.site_id\
                   FROM tests\
                   INNER JOIN dict_tests ON tests.test_id = dict_tests.test_id\
                   INNER JOIN samples ON dict_tests.sample_id = samples.sample_id\
                   INNER JOIN sections ON dict_tests.section_id = sections.section_id\
                   INNER JOIN labs ON sections.lab_id = labs.lab_id\
                   WHERE dict_test_id NOT IN ({0})\
                   AND labs.site_id ={1}\
                   AND tests.status =1\
                   AND dict_tests.status=1\
                   ORDER BY tests.description;".format(s ,self.related_ids[0])

        else:

            sql = "SELECT dict_tests.dict_test_id,\
                        tests.description || ' ' || samples.sample,\
                        labs.site_id\
                   FROM tests\
                   INNER JOIN dict_tests ON tests.test_id = dict_tests.test_id\
                   INNER JOIN samples ON dict_tests.sample_id = samples.sample_id\
                   INNER JOIN sections ON dict_tests.section_id = sections.section_id\
                   INNER JOIN labs ON sections.lab_id = labs.lab_id\
                   WHERE labs.site_id =?\
                   AND tests.status =1\
                   AND dict_tests.status=1\
                   ORDER BY tests.description;"

            args = (self.related_ids[0],)

        rs = self.nametowidget(".").engine.read(True, sql, args)
        index = 0
        self.dict_items = {}

        if rs:
            for i in rs:
                s = "{0}".format(i[1],)
                self.lstItems.insert(tk.END, s)
                self.dict_items[index] = i[0]
                index += 1

    def on_item_activated(self, evt=None):

        if self.lstItems.curselection():

            index = self.lstItems.curselection()[0]
            dict_test_id = self.dict_items.get(index)

            args = (self.selected_workstation[0], dict_test_id,)
            sql = "INSERT INTO dict_workstations (workstation_id, dict_test_id) values (?,?);"
            self.nametowidget(".").engine.write(sql, args)
            args = (self.selected_workstation[0],)

            if self.parent.winfo_name() == "data":
                self.parent.set_tests_methods(args)
            else:
                self.parent.set_tests_methods(args)

            self.tests_method_assigned.append(dict_test_id)
            self.set_values(self.tests_method_assigned)

        else:
            messagebox.showwarning(self.nametowidget(".").engine.title, self.nametowidget(".").engine.no_selected)

    def on_item_selected(self, evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.nametowidget(".").engine.get_selected("dict_tests", "dict_test_id", pk)

    def on_cancel(self, evt=None):
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()
