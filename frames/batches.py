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
import frames.load_tests_methods as load_tests_methods
import frames.batch as batch
import frames.result as result

class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="batches")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(400, 600)
        self.obj = None
        self.data = tk.StringVar()
        self.count_batchs = tk.StringVar()
        self.items = tk.StringVar()
        self.init_ui()
        self.nametowidget(".").engine.set_me_center(self)
        self.nametowidget(".").engine.set_instance(self, 1)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")

        frm_sections = ttk.Frame(frm_main,)
        cols = (["#0", "", "w", False, 200, 200],
                ["#1", "", "w", True, 0, 0],)
        self.Sites = self.nametowidget(".").engine.get_tree(frm_sections, cols, show="tree")
        self.Sites.show = "tree"
        self.Sites.pack(fill=tk.BOTH, padx=2, pady=2)
        self.Sites.bind("<<TreeviewSelect>>", self.on_branch_selected)
        self.Sites.bind("<Double-1>", self.on_branch_activated)


        frm_tests = ttk.Frame(frm_main,)
        w = tk.LabelFrame(frm_tests, text='Tests')
        cols = (["#0", 'test_method_id', 'w', False, 0, 0],
                ["#1", 'Test', 'w', True, 100, 100],
                ["#2", 'S', 'center', True, 50, 50],
                ["#3", 'Method', 'center', True, 50, 50],
                ["#4", 'Unit', 'center', True, 50, 50],)

        self.lstTestsMethods = self.nametowidget(".").engine.get_tree(w, cols)
        self.lstTestsMethods.bind("<<TreeviewSelect>>", self.on_test_method_selected)
        self.lstTestsMethods.bind("<Double-1>", self.on_test_method_activated)

        w.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm_batches = ttk.Frame(frm_main,)

        self.lblBatches = tk.LabelFrame(frm_batches, text='Batches')
        cols = (["#0", 'batch_id', 'w', False, 0, 0],
                ["#1", 'Control', 'w', True, 100, 100],
                ["#2", 'Lot', 'w', True, 80, 80],
                ["#3", 'Description', 'w', True, 100, 100],
                ["#4", 'Expiration', 'center', True, 80, 80],
                ["#5", 'Target', 'center', True, 80, 80],)

        self.lstBatches = self.nametowidget(".").engine.get_tree(self.lblBatches, cols)
        self.lstBatches.tag_configure('status', background=self.nametowidget(".").engine.get_rgb(211, 211, 211))
        self.lstBatches.bind("<<TreeviewSelect>>", self.on_batch_selected)
        self.lstBatches.bind("<Double-1>", self.on_batch_activated)

        self.lblBatches.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_sections.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_tests.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_batches.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

    def on_open(self,):
        
        msg = "{0} Management".format(self.winfo_name().title())
        self.title(msg)
        self.set_values()

    def on_reset(self):

        for i in self.lstTestsMethods.get_children():
            self.lstTestsMethods.delete(i)

        for i in self.lstBatches.get_children():
            self.lstBatches.delete(i)

        s = "{0} {1}".format("Batches", len(self.lstBatches.get_children()))
        self.lblBatches["text"] = s

    def set_values(self):

        if self.nametowidget(".").engine.log_user[5] ==0:

            sql = "SELECT DISTINCT(sites.supplier_id),suppliers.supplier\
                   FROM sites\
                   INNER JOIN suppliers ON suppliers.supplier_id = sites.supplier_id\
                   WHERE sites.status =1\
                   GROUP BY sites.supplier_id\
                   ORDER BY suppliers.supplier;"
            args = ()
        else:            

            sql = "SELECT sites.site_id,suppliers.supplier\
                   FROM sites\
                   INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id\
                   WHERE sites.supplier_id =?\
                   AND sites.status =1\
                   ORDER BY suppliers.supplier ASC;"

            section_id = self.nametowidget(".").engine.get_section_id()
            
            rs_idd = self.nametowidget(".").engine.get_idd_by_section_id(section_id)

            args = (rs_idd[1],)

        rs = self.nametowidget(".").engine.read(True, sql, args)

        #.insert(parent, index, iid=None, **kw)
        self.Sites.insert("", 0, 0, text="Sites")

        if self.nametowidget(".").engine.log_user[5] ==0:
            for i in rs:
                #print(i)
                sites = self.Sites.insert("", i[0], text=i[1], values=(i[0], "sites"))

                rs_hospitals = self.load_hospitals(i[0])

                if rs_hospitals is not None:

                    for hospital in rs_hospitals:

                        hospitals = self.Sites.insert(sites, hospital[0],
                                                      text=hospital[1],
                                                      values=(hospital[0], "hospitals"))
                        
                        rs_labs = self.load_wards(hospital[0])

                        if rs_labs is not None:

                            for lab in rs_labs:
                                labs = self.Sites.insert(hospitals, lab[0], text=lab[1], values=(lab[0], "labs"))
                                rs_sections = self.load_sections(lab[0])

                                if rs_sections is not None:

                                    for section in rs_sections:
                                        sections = self.Sites.insert(labs, section[0], text=section[1], values=(section[0], "sections"))
                                        rs_workstations = self.load_workstations(section[0])

                                        if rs_workstations is not None:
                                            for workstation in rs_workstations:
                                                self.Sites.insert(sections, workstation[0], text=workstation[1], values=(workstation[0], "workstations"))

                                

        else:

            for i in rs:
                sites = self.Sites.insert("", i[0], text=i[1], values=(i[0], "sites"))
                rs_labs = self.load_wards(i[0])

                if rs_labs is not None:

                    for lab in rs_labs:
                        labs = self.Sites.insert(sites, lab[0], text=lab[1], values=(lab[0], "labs"))
                        rs_sections = self.load_sections(lab[0])

                        if rs_sections is not None:

                            for section in rs_sections:
                                sections = self.Sites.insert(labs, section[0], text=section[1], values=(section[0], "sections"))
                                rs_workstations = self.load_workstations(section[0])

                                if rs_workstations is not None:

                                    for workstation in rs_workstations:
                                        self.Sites.insert(sections, workstation[0], text=workstation[1], values=(workstation[0], "workstations"))

    def load_hospitals(self, i):

        sql = "SELECT sites.site_id,suppliers.supplier\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id\
               WHERE sites.supplier_id =?\
               AND sites.status =1;"

        return self.nametowidget(".").engine.read(True, sql, (i,))
    
    def load_wards(self, site_id):

        sql = "SELECT lab_id, lab FROM labs WHERE site_id =? AND status =1 ORDER BY lab;"

        return self.nametowidget(".").engine.read(True, sql, (site_id,))

    def load_sections(self, lab_id):

        sql = "SELECT section_id, section FROM sections WHERE lab_id =? AND status =1 ORDER BY section;"

        return self.nametowidget(".").engine.read(True, sql, (lab_id,))

    def load_workstations(self, section_id):

        sql = "SELECT workstation_id, description FROM workstations WHERE section_id =? AND status =1 ORDER BY description;"

        return self.nametowidget(".").engine.read(True, sql, (section_id,))

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

                self.selected_workstation = self.nametowidget(".").engine.get_selected("workstations", "workstation_id", pk)

                self.obj = load_tests_methods.UI(self)

                self.obj.on_open(self.selected_workstation, self.tests_method_assigned)

    def set_tests_methods(self, args):

        self.tests_method_assigned = []

        self.on_reset()

        sql = "SELECT tests_methods.test_method_id,\
                      tests.description,\
                      IFNULL(samples.sample,'NA') AS samples,\
                      IFNULL(methods.method,'NA') AS methods,\
                      IFNULL(units.unit,'NA') AS units,\
                      workstations.description,\
                      workstations.status\
                FROM tests\
                INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
                INNER JOIN samples ON tests_methods.sample_id = samples.sample_id\
                INNER JOIN methods ON tests_methods.method_id = methods.method_id\
                INNER JOIN units ON tests_methods.unit_id = units.unit_id\
                INNER JOIN workstations_tests_methods ON tests_methods.test_method_id = workstations_tests_methods.test_method_id\
                INNER JOIN workstations ON workstations_tests_methods.workstation_id = workstations.workstation_id\
                WHERE workstations_tests_methods.workstation_id =?\
                AND tests.status =1\
                AND tests_methods.status =1\
                ORDER BY tests.description;"

        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:

            for i in rs:

                self.tests_method_assigned.append(i[0])

                if i[6] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("",)

                self.lstTestsMethods.insert('', tk.END, iid=i[0], text=i[0],
                                            values=(i[1], i[2], i[3], i[4], i[5]),
                                            tags=tag_config)

    def set_batches(self):

        for i in self.lstBatches.get_children():
            self.lstBatches.delete(i)

        sql = "SELECT batches.batch_id,\
                      controls.description,\
                      batches.lot_number,\
                      batches.description,\
                      strftime('%d-%m-%Y', expiration),\
                      ROUND(batches.target,3),\
                      batches.status\
               FROM batches\
               INNER JOIN controls ON batches.control_id = controls.control_id\
               WHERE batches.test_method_id =?\
               AND batches.workstation_id =?\
               AND batches.lot_number IS NOT NULL\
               AND batches.expiration IS NOT NULL\
               ORDER BY batches.expiration DESC, batches.ranck ASC;"

        args = (self.selected_test_method[0], self.selected_workstation[0])

        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:

            for i in rs:

                if i[6] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("",)

                self.lstBatches.insert('', tk.END, iid=i[0], text=i[0],
                                       values=(i[1], i[2], i[3], i[4], i[5]),
                                       tags=tag_config)

        s = "{0} {1}".format("Batches", len(self.lstBatches.get_children()))
        self.lblBatches["text"] = s

    def on_test_method_selected(self, evt=None):

        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            self.selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
            self.set_batches()

    def on_test_method_activated(self, evt=None):

        if self.lstTestsMethods.focus():

            self.on_add_batch()

    def on_batch_selected(self, evt=None):

        if self.lstBatches.focus():
            item_iid = self.lstBatches.selection()
            pk = int(item_iid[0])
            self.selected_batch = self.nametowidget(".").engine.get_selected("batches", "batch_id", pk)
            
    def on_batch_activated(self, evt):

        if self.lstBatches.focus():
            item_iid = self.lstBatches.selection()
            self.obj = batch.UI(self, item_iid)
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
            self.obj.on_open(selected_test_method, self.selected_workstation, self.selected_batch)

    def on_add_batch(self, evt=None):

        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)

            self.obj = batch.UI(self)
            self.obj.on_open(selected_test_method, self.selected_workstation,)

        else:
            msg = "Please select a test."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()
