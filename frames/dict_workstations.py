# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
import frames.load_tests_methods as ui


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="dict_workstations")

        #self.attributes("-topmost", True)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.obj = None
        self.nametowidget(".").engine.center_window_on_screen(self)
        self.init_ui()

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")
        
        frm_left = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        cols = (["#0", "", "w", False, 200, 200],
                ["#1", "", "w", True, 0, 0],)
        self.Sites = self.nametowidget(".").engine.get_tree(frm_left, cols, show="tree")
        self.Sites.show = "tree"
        self.Sites.pack(fill=tk.BOTH, padx=2, pady=2)
        self.Sites.bind("<<TreeviewSelect>>", self.on_branch_selected)
        self.Sites.bind("<Double-1>", self.on_branch_activated)        
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
        self.set_values()


    def set_values(self):

        sql = "SELECT sites.site_id,suppliers.description\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id\
               WHERE sites.supplier_id =?\
               AND sites.status =1\
               ORDER BY suppliers.description ASC;"

        section_id = self.nametowidget(".").engine.get_section_id()
        
        related_ids = self.nametowidget(".").engine.get_related_ids_by_section(section_id)

        args = (related_ids[1],)

        rs = self.nametowidget(".").engine.read(True, sql, args)

        #.insert(parent, index, iid=None, **kw)
        self.Sites.insert("", 0, 0, text="Sites")

        for i in rs:
            #print(i)
            sites = self.Sites.insert("",
                                      i[0],
                                      text=i[1],
                                      values=(i[0], "sites"))
            rs_labs = self.load_labs(i[0])

            if rs_labs is not None:

                for lab in rs_labs:
                    
                    labs = self.Sites.insert(sites,
                                              lab[0],
                                              text=lab[1],
                                              values=(lab[0], "labs"))

                    rs_sections = self.load_sections(lab[0])
                    
                    if rs_sections is not None:
                        
                        for section in rs_sections:
                            
                            sections = self.Sites.insert(labs,
                                              section[0],
                                              text=section[1],
                                              values=(section[0], "sections"))

                            rs_workstations = self.load_workstations(section[0])

                            if rs_workstations is not None:

                                for workstation in rs_workstations:
                                    self.Sites.insert(sections, workstation[0], text=workstation[1], values=(workstation[0], "workstations"))

    def load_labs(self, i):

        sql = "SELECT lab_id, lab\
               FROM labs\
               WHERE site_id =?\
               AND status =1"

        return self.nametowidget(".").engine.read(True, sql, (i,))

    def load_sections(self, i):

        sql = "SELECT section_id, section\
               FROM sections\
               WHERE lab_id =?\
               AND status =1"

        return self.nametowidget(".").engine.read(True, sql, (i,))

    def load_workstations(self, i):

        sql = "SELECT workstations.workstation_id,\
                      workstations.description\
               FROM workstations\
               INNER JOIN equipments ON workstations.equipment_id = equipments.equipment_id\
               WHERE workstations.section_id=?\
               AND workstations.status =1\
               ORDER BY workstations.description ASC;"

        return self.nametowidget(".").engine.read(True, sql, (i,))


    def on_branch_selected(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "workstations":

                pk = d["values"][0]

                self.selected_workstation = self.nametowidget(".").engine.get_selected("workstations", "workstation_id", pk)

                args = (self.selected_workstation[0],)

                self.set_tests_methods(args)

            
    def on_branch_activated(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "workstations":

                pk = d["values"][0]
                self.obj = ui.UI(self)
                self.obj.on_open(self.selected_workstation, self.tests_method_assigned)

   
    def set_tests_methods(self, args):

        self.tests_method_assigned = []

        for i in self.lstTestsMethods.get_children():
            self.lstTestsMethods.delete(i)
            
        sql = "SELECT dict_tests.dict_test_id,\
                      tests.description,\
                      dict_tests.code,\
                      IFNULL(samples.sample,'NA') AS samples,\
                      IFNULL(methods.method,'NA') AS methods,\
                      IFNULL(units.unit,'NA') AS units,\
                      dict_workstations.workstation_id\
               FROM tests\
               INNER JOIN dict_tests ON tests.test_id = dict_tests.test_id\
               INNER JOIN samples ON dict_tests.sample_id = samples.sample_id\
               INNER JOIN methods ON dict_tests.method_id = methods.method_id\
               INNER JOIN units ON dict_tests.unit_id = units.unit_id\
               INNER JOIN dict_workstations ON dict_tests.dict_test_id = dict_workstations.dict_test_id\
               INNER JOIN workstations ON dict_workstations.workstation_id = workstations.workstation_id\
               WHERE dict_workstations.workstation_id =?\
               ORDER BY tests.description ASC;"

        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:
            for i in rs:
                self.tests_method_assigned.append(i[0])
                self.lstTestsMethods.insert("", tk.END, iid=i[0], text=i[0],
                                        values=(i[1], i[2], i[3], i[4], i[5],),)
                         
    def on_test_method_activated(self, evt):

        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            dict_test_id = int(item_iid[0])
            args = (self.selected_workstation[0], dict_test_id)
            sql = "DELETE FROM dict_workstations WHERE workstation_id =? AND dict_test_id = ?"
            self.nametowidget(".").engine.write(sql, args)
            args = (self.selected_workstation[0], )
            self.set_tests_methods(args)

            if self.nametowidget(".").engine.get_instance("load_tests_methods") == True:
                self.obj.on_open(self.selected_workstation, self.tests_method_assigned)    
            
    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
