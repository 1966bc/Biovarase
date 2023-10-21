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
import frames.load_tests_methods as ui


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="workstations_tests_methods")

        #self.attributes("-topmost", True)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.obj = None
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")
        
        frm_left = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)


        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Workstation", "w", True, 100, 100],
                ["#2", "Ward", "w", True, 80, 80],
                ["#3", "Section", "w", True, 80, 80],)

        self.lstVorkstations = self.nametowidget(".").engine.get_tree(frm_left, cols,)
        self.lstVorkstations.tag_configure("status", background="light gray")
        self.lstVorkstations.bind("<<TreeviewSelect>>", self.on_workstation_selected)
        self.lstVorkstations.bind("<Double-1>", self.on_workstation_activated)
        
        frm_right = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Test", "w", True, 100, 100],
                ["#2", "Code", "w", True, 100, 100],
                ["#3", "Sample", "w", True, 50, 50],
                ["#4", "Method", "w", True, 100, 100],
                ["#5", "Unit", "w", True, 80, 80],)

        self.lstTestsMethods = self.nametowidget(".").engine.get_tree(frm_right, cols,)
        self.lstTestsMethods.tag_configure("status", background="light gray")
        self.lstTestsMethods.bind("<Double-1>", self.on_test_method_activated)

        frm_main.pack(fill=tk.BOTH, expand=1)
        frm_left.pack(side=tk.LEFT, fill=tk.Y,expand=0)
        frm_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def on_open(self,):

        msg = "Workstations Test Methods Management"
        self.title(msg)
        self.set_workstations()

    def set_workstations(self, evt=None):

        for i in self.lstVorkstations.get_children():
            self.lstVorkstations.delete(i)

        sql = "SELECT workstations.workstation_id,\
                      workstations.description,\
                      wards.ward,\
                      sections.section,\
                      workstations.status\
               FROM workstations\
               INNER JOIN equipments ON workstations.equipment_id = equipments.equipment_id\
               INNER JOIN sections ON workstations.section_id = sections.section_id\
               INNER JOIN wards ON sections.ward_id = wards.ward_id\
               WHERE sections.section_id=?\
               AND workstations.status =1\
               ORDER BY workstations.description ASC;"

        site_id = self.nametowidget(".").engine.get_section_id()

        args = (site_id,)
        
        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:
            for i in rs:
                if i[4] != 1:
                    tag_config = ("status",)    
                else:
                    tag_config = ("",)            

                self.lstVorkstations.insert("", tk.END, iid=i[0], text=i[0],
                                        values=(i[1],i[2],i[3]),
                                        tags = tag_config)

    def set_tests_methods(self, args):

        self.tests_method_assigned = []

        for i in self.lstTestsMethods.get_children():
            self.lstTestsMethods.delete(i)
            

        sql = "SELECT tests_methods.test_method_id,\
                      tests.test,\
                      tests_methods.code,\
                      IFNULL(samples.sample,'NA') AS samples,\
                      IFNULL(methods.method,'NA') AS methods,\
                      IFNULL(units.unit,'NA') AS units,\
                      workstations_tests_methods.workstation_id\
               FROM tests\
               INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
               INNER JOIN samples ON tests_methods.sample_id = samples.sample_id\
               INNER JOIN methods ON tests_methods.method_id = methods.method_id\
               INNER JOIN units ON tests_methods.unit_id = units.unit_id\
               INNER JOIN workstations_tests_methods ON tests_methods.test_method_id = workstations_tests_methods.test_method_id\
               INNER JOIN workstations ON workstations_tests_methods.workstation_id = workstations.workstation_id\
               WHERE workstations_tests_methods.workstation_id =?\
               ORDER BY tests.test ASC;"

        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:
            for i in rs:
                self.tests_method_assigned.append(i[0])
                self.lstTestsMethods.insert("", tk.END, iid=i[0], text=i[0],
                                        values=(i[1], i[2], i[3], i[4], i[5],),)
                
    def on_workstation_selected(self, evt):

        if self.lstVorkstations.focus():
            item_iid = self.lstVorkstations.selection()
            pk = int(item_iid[0])
            self.selected_workstation = self.nametowidget(".").engine.get_selected("workstations", "workstation_id", pk)
   
            args = (self.selected_workstation[0],)
            self.set_tests_methods(args)

    def on_workstation_activated(self, evt):

        if self.lstVorkstations.focus():
            item_iid = self.lstVorkstations.selection()
            pk = int(item_iid[0])
            selected_item = self.nametowidget(".").engine.get_selected("workstations", "workstation_id", pk)
            self.obj = ui.UI(self)
            self.obj.on_open(self.selected_workstation, self.tests_method_assigned)
            
    def on_test_method_activated(self, evt):

        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            test_method_id = int(item_iid[0])
            args = (self.selected_workstation[0], test_method_id)
            sql = "DELETE FROM workstations_tests_methods WHERE workstation_id =? AND test_method_id = ?"
            self.nametowidget(".").engine.write(sql, args)
            args = (self.selected_workstation[0], )
            self.set_tests_methods(args)

            if self.nametowidget(".").engine.get_instance("load_tests_methods") == True:
                self.obj.on_open(self.selected_workstation, self.tests_method_assigned)    
            
    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
