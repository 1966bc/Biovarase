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
        super().__init__(name="data")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(400, 600)
        self.obj = None
        self.data = tk.StringVar()
        self.count_batchs = tk.StringVar()
        self.items = tk.StringVar()
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)
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

        frm_results = ttk.Frame(frm_main,)
        ttk.Label(frm_results, style='App.TLabel', textvariable=self.items,).pack(fill=tk.X, expand=0)

        sb = ttk.Scrollbar(frm_results, orient=tk.VERTICAL)
        self.lstResults = tk.Listbox(frm_results, yscrollcommand=sb.set,)
        self.lstResults.bind("<<ListboxSelect>>", self.on_result_selected)
        self.lstResults.bind("<Double-Button-1>", self.on_result_activated)
        sb.config(command=self.lstResults.yview)
        self.lstResults.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)


        frm_buttons = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        bts = (("Batch", 0, self.on_add_batch, "<Alt-b>"),
               ("Result", 0, self.on_add_result, "<Alt-r>"),
               ("Delete", 0, self.on_delete, "<Alt-d>"),
               ("Cancel", 0, self.on_cancel, "<Alt-c>"))

        for btn in bts:
            ttk.Button(frm_buttons,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])

        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_sections.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_tests.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_batches.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_results.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)

    def on_open(self,):

        msg = ("Results: {0}".format(self.lstResults.size()))
        self.items.set(msg)   
        self.title("Batches and Results Management")

        sql = "SELECT sites.site_id,suppliers.supplier AS site\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id"

        rs = self.nametowidget(".").engine.read(True, sql, ())

        if rs:
            self.set_values(rs)

    def on_reset(self):

        for i in self.lstTestsMethods.get_children():
            self.lstTestsMethods.delete(i)

        for i in self.lstBatches.get_children():
            self.lstBatches.delete(i)

        s = "{0} {1}".format("Batches", len(self.lstBatches.get_children()))
        self.lblBatches["text"] = s

        self.lstResults.delete(0, tk.END)

    def set_values(self, rs):

        #.insert(parent, index, iid=None, **kw)
        self.Sites.insert("", 0, 0, text="Sites")

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

    def load_wards(self, site_id):

        sql = "SELECT ward_id, ward FROM wards WHERE site_id =? AND status =1;"

        return self.nametowidget(".").engine.read(True, sql, (site_id,))

    def load_sections(self, ward_id):

        sql = "SELECT section_id, section FROM sections WHERE ward_id =? AND status =1;"

        return self.nametowidget(".").engine.read(True, sql, (ward_id,))

    def load_workstations(self, section_id):

        sql = "SELECT workstation_id, description FROM workstations WHERE section_id =? AND status =1;"

        return self.nametowidget(".").engine.read(True, sql, (section_id,))

    def on_branch_selected(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "workstations":

                pk = d["values"][0]

                self.selected_workstation = self.nametowidget(".").engine.get_selected("workstations", "workstation_id", pk)

                self.section_data = self.nametowidget(".").engine.get_section_data(self.selected_workstation[4])

                args = (self.selected_workstation[0],)

                self.set_tests_methods(args)

            else:
                self.on_reset()

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

        self.lstResults.delete(0, tk.END)

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

    def set_results(self):

        self.lstResults.delete(0, tk.END)
        index = 0
        self.dict_results = {}

        sql = "SELECT results.result_id,\
                      ROUND(results.result,3),\
                      strftime('%d-%m-%Y', recived),\
                      results.status\
               FROM results\
               WHERE results.batch_id =?\
               AND results.workstation_id=?\
               AND results.is_delete =0\
               ORDER BY results.recived DESC"

        args = (self.selected_batch[0], self.selected_workstation[0])

        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:
            for i in rs:

                s = '{0:10}{1:14}'.format(i[2], i[1])
                self.lstResults.insert(tk.END, s)
                if i[3] != 1:
                    self.lstResults.itemconfig(index, {"bg":"light gray"})
                self.dict_results[index] = i[0]
                index += 1

        msg = ("Results: {0}".format(self.lstResults.size()))
        self.items.set(msg)                

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
            self.set_results()

    def on_batch_activated(self, evt):

        if self.lstBatches.focus():
            item_iid = self.lstBatches.selection()
            self.obj = batch.UI(self, item_iid)
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
            self.obj.on_open(selected_test_method, self.selected_workstation, self.selected_batch)

    def on_result_selected(self, evt):

        if self.lstResults.curselection():
            index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(index)
            self.selected_result = self.nametowidget(".").engine.get_selected("results", "result_id", pk)
            
    def on_result_activated(self, evt=None):

        if self.lstResults.curselection():

            index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(index)
            selected_result = self.nametowidget(".").engine.get_selected("results", "result_id", pk)

            self.obj = result.UI(self, index)

            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
            item_iid = self.lstBatches.selection()
            pk = int(item_iid[0])
            selected_batch = self.nametowidget(".").engine.get_selected("batches", "batch_id", pk)

            self.obj.on_open(selected_test_method,
                             selected_batch,
                             self.selected_workstation,
                             selected_result)

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

    def on_add_result(self, evt=None):

        if self.lstBatches.focus():

            item_iid = self.lstBatches.selection()
            pk = int(item_iid[0])
            selected_batch = self.nametowidget(".").engine.get_selected("batches", "batch_id", pk)

            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
            self.obj = result.UI(self)
            self.obj.on_open(selected_test_method, selected_batch, self.selected_workstation)

        else:
            msg = "Please select a batch."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

    def  on_delete(self, evt=None):

        if self.lstResults.focus():
            results_id = self.lstResults.selection()

            if messagebox.askyesno(self.nametowidget(".").title(), self.nametowidget(".").engine.ask_to_delete, parent=self) == True:
                sql = "UPDATE results SET is_delete =1 WHERE result_id =?"

                for i in results_id:
                    args = (i,)
                    self.nametowidget(".").engine.write(sql, args)

                self.update_main()
                self.update_data(args)

            else:
                messagebox.showinfo(self.nametowidget(".").title(), self.nametowidget(".").engine.abort, parent=self)
        else:
            msg = "Please select results."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

    def update_main(self):

        try:
            self.nametowidget(".main").set_results()
        except:
            pass

    def update_data(self,args):

        if self.nametowidget(".").engine.get_instance("data") == True:

            try:
                if args[2] == self.nametowidget(".data").selected_workstation[0]:

                    if self.nametowidget(".data").selected_test_method[0] == self.selected_test_method[0]:

                        self.nametowidget(".data").set_results()

            except AttributeError:
                pass         

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()
