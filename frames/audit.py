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
    def __init__(self, parent,):
        super().__init__(name="audit")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(400, 600)
        self.obj = None
        self.init_ui()
        self.center_me()
        self.nametowidget(".").engine.set_instance(self, 1)

    def center_me(self,):
        """center window on the screen"""

        x = self.parent.winfo_rootx()
        y = self.parent.winfo_rooty()
        self.geometry("+%d+%d" % (x, y))     

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")

        frm_sections = ttk.Frame(frm_main,)
        cols = (["#0", "", "w", False, 200, 200],
                ["#1", "", "w", True, 0, 0],)
        self.Sites = self.nametowidget(".").engine.get_tree(frm_sections, cols, show="tree")
        self.Sites.show = "tree"
        self.Sites.pack(fill=tk.BOTH, padx=2, pady=2)
        self.Sites.bind("<<TreeviewSelect>>", self.on_branch_selected)
        
        frm_tests = ttk.Frame(frm_main,)
        w = tk.LabelFrame(frm_tests, text='Tests')
        cols = (["#0", 'test_method_id', 'w', False, 0, 0],
                ["#1", 'Test', 'w', True, 100, 100],
                ["#2", 'S', 'center', True, 50, 50],
                ["#3", 'Method', 'center', True, 50, 50],
                ["#4", 'Unit', 'center', True, 50, 50],)

        self.lstTestsMethods = self.nametowidget(".").engine.get_tree(w, cols)
        self.lstTestsMethods.bind("<<TreeviewSelect>>", self.on_test_method_selected)
        
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm_audits = ttk.Frame(frm_main,)
        
        self.lblBatches = tk.LabelFrame(frm_audits, text='Batches')
        
        cols = (["#0", 'batch_id', 'w', False, 0, 0],
                ["#1", 'Control', 'w', True, 0, 80],
                ["#2", 'Lot', 'w', True, 0, 80],
                ["#3", 'Description', 'w', True, 0, 80],
                ["#4", 'Expiration', 'center', True, 0, 80],
                ["#5", 'Target', 'center', True, 0, 80],
                ["#6", 'Log time', 'center', True, 0, 100],
                ["#7", 'Log id', 'center', True, 0, 100],
                ["#8", 'Log ip', 'center', True, 0, 100],)

        self.lstBatches = self.nametowidget(".").engine.get_tree(self.lblBatches, cols)
        self.lstBatches.tag_configure('status', background=self.nametowidget(".").engine.get_rgb(211, 211, 211))
        self.lstBatches.bind("<<TreeviewSelect>>", self.on_batch_selected)

        self.lblBatches.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.lblResults = tk.LabelFrame(frm_audits, text='Results')

        cols = (["#0", 'result_id', 'w', False, 0, 0],
                ["#1", 'Run', 'w', True, 0, 80],
                ["#2", 'Result', 'w', True, 0, 80],
                ["#3", 'Recived', 'w', True, 0, 80],
                ["#4", 'Log time', 'center', True, 0, 100],
                ["#5", 'Log id', 'center', True, 0, 100],
                ["#6", 'Log ip', 'center', True, 0, 100],)

        self.lstResults = self.nametowidget(".").engine.get_tree(self.lblResults, cols)
        self.lstResults.tag_configure('status', background=self.nametowidget(".").engine.get_rgb(211, 211, 211))
        self.lblResults.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_sections.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_tests.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_audits.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        
    def on_open(self,):
        
        self.title("Audit Trails")
        self.set_values()

    def on_reset(self):

        for i in self.lstTestsMethods.get_children():
            self.lstTestsMethods.delete(i)

        for i in self.lstBatches.get_children():
            self.lstBatches.delete(i)

        for i in self.lstResults.get_children():
            self.lstResults.delete(i)

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
                        
                        rs_wards = self.load_wards(hospital[0])

                        if rs_wards is not None:

                            for ward in rs_wards:
                                wards = self.Sites.insert(hospitals, ward[0], text=ward[1], values=(ward[0], "wards"))
                                rs_sections = self.load_sections(ward[0])

                                if rs_sections is not None:

                                    for section in rs_sections:
                                        sections = self.Sites.insert(wards, section[0], text=section[1], values=(section[0], "sections"))
                                        rs_workstations = self.load_workstations(section[0])

                                if rs_workstations is not None:
                                    for workstation in rs_workstations:
                                        self.Sites.insert(sections, workstation[0], text=workstation[1], values=(workstation[0], "workstations"))

        else:

            for i in rs:
                sites = self.Sites.insert("", i[0], text=i[1], values=(i[0], "sites"))
                rs_wards = self.load_wards(i[0])

                if rs_wards is not None:

                    for ward in rs_wards:
                        wards = self.Sites.insert(sites, ward[0], text=ward[1], values=(ward[0], "wards"))
                        rs_sections = self.load_sections(ward[0])

                        if rs_sections is not None:

                            for section in rs_sections:
                                sections = self.Sites.insert(wards, section[0], text=section[1], values=(section[0], "sections"))
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

        sql = "SELECT ward_id, ward FROM wards WHERE site_id =? AND status =1 ORDER BY ward;"

        return self.nametowidget(".").engine.read(True, sql, (site_id,))

    def load_sections(self, ward_id):

        sql = "SELECT section_id, section FROM sections WHERE ward_id =? AND status =1 ORDER BY section;"

        return self.nametowidget(".").engine.read(True, sql, (ward_id,))

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

    def set_tests_methods(self, args):

        self.tests_method_assigned = []

        self.on_reset()

        sql = "SELECT tests_methods.test_method_id,\
                      tests.test,\
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
                ORDER BY tests.test;"

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

        for i in self.lstResults.get_children():
            self.lstResults.delete(i)            

        sql = "SELECT audit_batches.batch_id,\
                      controls.description,\
                      audit_batches.lot_number,\
                      audit_batches.description,\
                      strftime('%d-%m-%Y', expiration) AS expiration,\
                      ROUND(audit_batches.target,3) AS target,\
		      audit_batches.log_time,\
		      users.last_name||' '|| users.first_name AS log_id,\
		      audit_batches.log_ip,\
                      audit_batches.status\
               FROM audit_batches\
               INNER JOIN controls ON audit_batches.control_id = controls.control_id\
	       INNER JOIN users ON audit_batches.log_id = users.user_id\
               WHERE audit_batches.test_method_id =?\
               AND audit_batches.workstation_id =?\
               ORDER BY audit_batches.log_time;"

        args = (self.selected_test_method[0], self.selected_workstation[0])

        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:

            for i in rs:

                if i[9] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("",)

                self.lstBatches.insert('', tk.END, text=i[0],
                                       values=(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]),
                                       tags=tag_config)

        s = "{0} {1}".format("Batches trails", len(self.lstBatches.get_children()))
        self.lblBatches["text"] = s

    def set_results(self):

        for i in self.lstResults.get_children():
            self.lstResults.delete(i)           

        sql = "SELECT audit_results.result_id,\
                      audit_results.run_number,\
                      ROUND(audit_results.result,3) AS result,\
                      strftime('%d-%m-%Y', audit_results.recived) AS recived,\
		      audit_results.log_time,\
		      users.last_name ||' '|| users.first_name AS log_id,\
		      audit_results.log_ip,\
                      audit_results.status\
               FROM audit_results\
	       INNER JOIN users ON audit_results.log_id = users.user_id\
               WHERE audit_results.batch_id =?\
               AND audit_results.workstation_id =?\
               ORDER BY audit_results.log_time;"

        args = (self.selected_batch, self.selected_workstation[0])

        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:

            for i in rs:

                if i[7] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("",)

                self.lstResults.insert('', tk.END, text=i[0],
                                       values=(i[1], i[2], i[3], i[4], i[5], i[6]),
                                       tags=tag_config)

        s = "{0} {1}".format("Results trails", len(self.lstResults.get_children()))
        self.lblResults["text"] = s

    def on_test_method_selected(self, evt=None):

        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            self.selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
            self.set_batches()

    def on_batch_selected(self, evt=None):

        if self.lstBatches.focus():
            selected_item = self.lstBatches.focus()
            dict_item =  self.lstBatches.item(selected_item)
            self.selected_batch = int(dict_item["text"])
            self.set_results()

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()
