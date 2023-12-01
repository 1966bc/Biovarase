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
        self.nametowidget(".").engine.center_me(self)
        self.nametowidget(".").engine.set_instance(self, 1)

    def init_ui(self):

        f0 = ttk.Frame(self, style="App.TFrame", padding=8)
        self.lstItems = self.nametowidget(".").engine.get_listbox(f0, color="light yellow")
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        f0.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)

    def on_open(self, selected_workstation, tests_method_assigned):

        self.rs_idd = self.nametowidget(".").engine.get_idd_by_section_id(selected_workstation[5])

        comp_id = self.rs_idd[2]

        self.selected_workstation = selected_workstation
        self.tests_method_assigned = tests_method_assigned
        args = (selected_workstation[0],)
        self.set_values(tests_method_assigned)

        sql = "SELECT sites.site_id, suppliers.supplier AS site\
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

            sql = "SELECT tests_methods.test_method_id,\
                        tests.test || ' ' || samples.sample,\
                        labs.site_id\
                   FROM tests\
                   INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
                   INNER JOIN samples ON tests_methods.sample_id = samples.sample_id\
                   INNER JOIN sections ON tests_methods.section_id = sections.section_id\
                   INNER JOIN labs ON sections.lab_id = labs.lab_id\
                   WHERE test_method_id NOT IN ({0})\
                   AND labs.site_id ={1}\
                   AND tests.status =1\
                   AND tests_methods.status=1\
                   ORDER BY tests.test;".format(s ,self.rs_idd[0])

        else:

            sql = "SELECT tests_methods.test_method_id,\
                        tests.test || ' ' || samples.sample,\
                        labs.site_id\
                   FROM tests\
                   INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
                   INNER JOIN samples ON tests_methods.sample_id = samples.sample_id\
                   INNER JOIN sections ON tests_methods.section_id = sections.section_id\
                   INNER JOIN labs ON sections.lab_id = labs.lab_id\
                   WHERE labs.site_id =?\
                   AND tests.status =1\
                   AND tests_methods.status=1\
                   ORDER BY tests.test;"

            args = (self.rs_idd[0],)

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
            test_method_id = self.dict_items.get(index)

            args = (self.selected_workstation[0], test_method_id,)
            sql = "INSERT INTO workstations_tests_methods (workstation_id, test_method_id) values (?,?);"
            self.nametowidget(".").engine.write(sql, args)
            args = (self.selected_workstation[0],)

            if self.parent.winfo_name() == "data":
                self.parent.set_tests_methods(args)
            else:
                self.parent.set_tests_methods(args)

            self.tests_method_assigned.append(test_method_id)
            self.set_values(self.tests_method_assigned)

        else:
            messagebox.showwarning(self.nametowidget(".").engine.title, self.nametowidget(".").engine.no_selected)

    def on_item_selected(self, evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)

    def on_cancel(self, evt=None):
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()
