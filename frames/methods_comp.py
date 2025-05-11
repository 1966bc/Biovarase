# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="methods_comp")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(400, 600)
        self.obj = None
        self.data = tk.StringVar()
        self.count_batchs = tk.StringVar()
        self.items = tk.StringVar()
        self.option_id = tk.IntVar()
        self.test_y = tk.StringVar()
        self.workstation_y = tk.StringVar()
        self.test_x = tk.StringVar()
        self.workstation_x = tk.StringVar()
        self.dict_test_selected = {}
        self.dict_compare_selected = {}
        self.init_ui()
        self.nametowidget(".").engine.center_window_on_screen(self)
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

        frm_tests = ttk.Frame(frm_main,)
        w = tk.LabelFrame(frm_tests, text='Tests')
        cols = (["#0", 'dict_test_id', 'w', False, 0, 0],
                ["#1", 'Test', 'w', True, 100, 100],
                ["#2", 'S', 'center', True, 50, 50],
                ["#3", 'Method', 'center', True, 50, 50],
                ["#4", 'Unit', 'center', True, 50, 50],)

        self.lstTestsMethods = self.nametowidget(".").engine.get_tree(w, cols)
        self.lstTestsMethods.bind("<<TreeviewSelect>>", self.on_test_method_selected)
        self.lstTestsMethods.bind("<Double-1>", self.on_test_method_activated)

        w.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm_selected = ttk.Frame(frm_main,)
        w = ttk.LabelFrame(frm_selected, style="App.TLabelframe", text='Selected tests to compare')
        
        ttk.Label(w, style="App.TLabel", text="Test Y",).pack(anchor=tk.W)
        ttk.Entry(w, textvariable=self.test_y).pack(anchor=tk.W)
        ttk.Label(w, style="App.TLabel", text="Workstation Y",).pack(anchor=tk.W)
        ttk.Entry(w, textvariable=self.workstation_y).pack(anchor=tk.W)
        
        ttk.Label(w, style="App.TLabel", text="Compare X",).pack(anchor=tk.W)
        ttk.Entry(w, textvariable=self.test_x).pack(anchor=tk.W)
        ttk.Label(w, style="App.TLabel", text="Workstation X",).pack(anchor=tk.W)
        ttk.Entry(w, textvariable=self.workstation_x).pack(anchor=tk.W)

        w.pack(side=tk.TOP, fill=tk.Y, expand=1)

        frm_buttons = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        bts = (("Reset", 0, self.on_reset, "<Alt-r>"),
               ("Create", 1, self.on_create_experiment, "<Alt-e>"),
               ("Cancel", 0, self.on_cancel, "<Alt-c>"))

        for btn in bts:
            ttk.Button(frm_buttons,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])


        frm_choice = ttk.LabelFrame(frm_buttons, style="App.TLabelframe", text="To select",)

        voices = ["Test", "Compare",]
        for index, text in enumerate(voices):
            ttk.Radiobutton(frm_choice,
                            style="App.TRadiobutton",
                            text=text,
                            variable=self.option_id,
                            value=index,).pack(anchor=tk.W)
            
        frm_choice.pack()

        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_sections.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_tests.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_selected.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        
    def on_open(self,):

        self.title("Choice Tests Method To Compare")
        self.set_values()

    def on_reset(self):
        self.dict_test_selected = {}
        self.dict_compare_selected= {}
        self.test_y.set("")
        self.workstation_y.set("")
        self.test_x.set("")
        self.workstation_x.set("")
        
    def set_values(self):

        if self.nametowidget(".").engine.log_user[5] ==0:

            sql = "SELECT DISTINCT(sites.supplier_id),suppliers.description\
                   FROM sites\
                   INNER JOIN suppliers ON suppliers.supplier_id = sites.supplier_id\
                   WHERE sites.status =1\
                   GROUP BY sites.supplier_id\
                   ORDER BY suppliers.description;"
            
            args = ()
            
        else:            

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
                        
                        rs_labs = self.load_labs(hospital[0])

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
                rs_labs = self.load_labs(i[0])

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

        sql = "SELECT sites.site_id,suppliers.description\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id\
               WHERE sites.supplier_id =?\
               AND sites.status =1;"

        return self.nametowidget(".").engine.read(True, sql, (i,))
    
    def load_labs(self, site_id):

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


    def set_tests_methods(self, args):

        for i in self.lstTestsMethods.get_children():
            self.lstTestsMethods.delete(i)

        sql = "SELECT dict_tests.dict_test_id,\
                      tests.description,\
                      IFNULL(samples.sample,'NA') AS samples,\
                      IFNULL(methods.method,'NA') AS methods,\
                      IFNULL(units.unit,'NA') AS units\
                FROM tests\
                INNER JOIN dict_tests ON tests.test_id = dict_tests.test_id\
                INNER JOIN samples ON dict_tests.sample_id = samples.sample_id\
                INNER JOIN methods ON dict_tests.method_id = methods.method_id\
                INNER JOIN units ON dict_tests.unit_id = units.unit_id\
                INNER JOIN dict_workstations ON dict_tests.dict_test_id = dict_workstations.dict_test_id\
                INNER JOIN workstations ON dict_workstations.workstation_id = workstations.workstation_id\
                WHERE dict_workstations.workstation_id =?\
                AND tests.status =1\
                AND dict_tests.status =1\
                ORDER BY tests.description;"

        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:
            for i in rs:
                self.lstTestsMethods.insert('', tk.END, iid=i[0], text=i[0],
                                            values=(i[1], i[2], i[3], i[4]),)

  
    def on_test_method_selected(self, evt=None):

        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            self.selected_test_method = self.nametowidget(".").engine.get_selected("dict_tests", "dict_test_id", pk)
            

    def on_test_method_activated(self, evt=None):

        if self.lstTestsMethods.focus():
            
            if self.option_id.get() == 0:
                self.dict_test_selected = {0:self.selected_workstation,
                                           1:self.selected_test_method}
                args = (self.dict_test_selected[1][0],)
                rs = self.get_test_data(args)
                msg = "{0} {1} {2} {3}".format(rs[0], rs[1], rs[2], rs[3],)
                self.test_y.set(msg) 
                self.workstation_y.set(self.dict_test_selected[0][3])

            elif self.option_id.get() == 1:
                self.dict_compare_selected = {0:self.selected_workstation,
                                              1:self.selected_test_method}
                args = (self.dict_compare_selected[1][0],)
                rs = self.get_test_data(args)
                msg = "{0} {1} {2} {3}".format(rs[0], rs[1], rs[2], rs[3],)
                self.test_x.set(msg) 
                self.workstation_x.set(self.dict_compare_selected[0][3])

    def on_create_experiment(self,):
        
        if not self.dict_test_selected:
            msg = "You have to choose a test before going on."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
            return
        elif not self.dict_compare_selected:
            msg = "You have to choose a method to compare before going on."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
            return

        else:
            msg = "Create a new experiment for selected tests?."
            if messagebox.askyesno(self.nametowidget(".").title(), msg, parent=self) == True:
                test_id = self.dict_test_selected[1][1]
                x_test_method_id = self.dict_test_selected[1][0]
                y_comp_method_id = self.dict_compare_selected[1][0]
                x_workstation_id_test = self.dict_test_selected[0][0]
                y_workstation_id_comp = self.dict_compare_selected[0][0]
                args = (test_id,
                        x_test_method_id,
                        y_comp_method_id,
                        x_workstation_id_test,
                        y_workstation_id_comp,
                        0,
                        0,
                        1,
                        self.nametowidget(".").engine.get_log_time(),
                        self.nametowidget(".").engine.get_log_id(),
                        self.nametowidget(".").engine.get_log_ip())
                
                sql =  self.nametowidget(".").engine.get_insert_sql("methods_comp", len(args))
                
                self.nametowidget(".").engine.write(sql, args)

                self.parent.set_experiments()

                self.on_cancel()
                
    def get_test_data(self, args):

        sql = "SELECT tests.description,\
                      IFNULL(samples.sample,'NA') AS samples,\
                      IFNULL(methods.method,'NA') AS methods,\
                      IFNULL(units.unit,'NA') AS units\
               FROM tests\
               INNER JOIN dict_tests ON tests.test_id = dict_tests.test_id\
               INNER JOIN samples ON dict_tests.sample_id = samples.sample_id\
               INNER JOIN methods ON dict_tests.method_id = methods.method_id\
               INNER JOIN units ON dict_tests.unit_id = units.unit_id\
               WHERE dict_tests.dict_test_id =?;"

        return self.nametowidget(".").engine.read(False, sql, args)
         

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()
