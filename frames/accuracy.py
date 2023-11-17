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
import numpy as np 
import matplotlib.pyplot as plt 
import scipy.stats

import frames.methods_comp
import frames.comparisions
import frames.bland_altman
import frames.methods_comp_result


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="accuracy")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(800, 600)
        self.code = tk.StringVar()
        self.objs = []
        self.option_id = tk.IntVar()
        self.status = tk.IntVar()
        self.actions = tk.IntVar()
        self.items = tk.StringVar()
        self.pcc = tk.StringVar()
        self.experiments = tk.StringVar()
        self.init_ui()
        self.nametowidget(".").engine.set_me_center(self)
        self.nametowidget(".").engine.set_instance(self, 1)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")
        frm_left = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        frm_experiments = ttk.Frame(frm_left, style="App.TFrame")
        ttk.Label(frm_experiments, textvariable = self.experiments, anchor=tk.W)
        cols = (["#0", "Experiment ID", "w", False, 0, 0],
                ["#1", "Site", "w", True, 0, 100],
                ["#2", "Ward", "w", True, 0, 100],
                ["#3", "Section", "w", True, 0, 100],
                ["#4", "Test", "w", True, 0, 100],
                ["#5", "Test Method Y", "w", True, 0, 80],
                ["#6", "Workstation Y", "w", True, 0, 80],
                ["#7", "Comp Method X", "w", True, 0, 80],
                ["#8", "Workstation X", "w", True, 0, 80],
                ["#9", "Created", "w", True, 0, 80],)
        self.lstExperiments = self.nametowidget(".").engine.get_tree(frm_experiments, cols)
        self.lstExperiments.tag_configure("passed", background="#90EE90")
        self.lstExperiments.tag_configure("not_passed", background="#FF7F7F")
        #self.lstExperiments.tag_configure("computed", background="yellow")
        self.lstExperiments.bind("<<TreeviewSelect>>", self.on_experiment_selected)
        self.lstExperiments.bind("<Double-1>", self.on_experiment_activated)
        frm_experiments.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        
        frm_results = ttk.Frame(frm_left, style="App.TFrame", relief=tk.GROOVE, padding=8)
        ttk.Label(frm_results, textvariable=self.items, anchor=tk.W)
        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Test (Y)", "center", True, 0, 50],
                ["#2", "Comp (X)", "center", True, 0, 50],
                ["#3", "Recived", "center", True, 0, 100],)
        
        self.lstResults = self.nametowidget(".").engine.get_tree(frm_results, cols)
        self.lstResults.tag_configure("status", background="light gray")
        self.lstResults.bind("<<TreeviewSelect>>", self.on_result_selected)
        self.lstResults.bind("<Double-1>", self.on_result_activated)
        frm_results.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        
        frm_buttons = ttk.Frame(frm_main, style="App.TFrame", padding=4)
        bts = [("Experiment",0, self.on_experiment, "<Alt-e>"),
               ("Result",0, self.on_result, "<Alt-r>"),
               ("Compute",1, self.on_compute, "<Alt-o>"),
               ("Comparisions",0, self.on_comparisions, "<Alt-p>"),
               ("Differences",0, self.on_differences, "<Alt-d>"),
               ("Close",0, self.on_cancel, "<Alt-c>")]

        for btn in bts:
            ttk.Button(frm_buttons,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command = btn[2]).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])

        
        w = ttk.LabelFrame(frm_buttons, style="App.TLabelframe", text='PCC',)
        ttk.Label(w,style="App.TLabel", textvariable = self.pcc).pack(side=tk.TOP)
        w.pack(side=tk.TOP, fill=tk.X, expand=0)
        
        frm_main.pack(fill=tk.BOTH, expand=1)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        
    def on_open(self,):

        self.title("Accuracy")
        
        self.on_reset()

    def on_reset(self, evt=None):

        self.set_experiments()
        
        self.items.set("Results")

    def on_experiment(self, evt=None):
        obj = frames.methods_comp.UI(self)
        obj.on_open()
        self.objs.append(obj)

    def on_result(self, evt=None):

        if self.lstExperiments.focus():

             obj = frames.methods_comp_result.UI(self)
             obj.on_open()
             self.objs.append(obj)
              
    def set_experiments(self):

        self.correlation_coefficient = self.nametowidget(".").engine.get_correlation_coefficient()

        for i in self.lstExperiments.get_children():
            self.lstExperiments.delete(i)

        for i in self.lstResults.get_children():
            self.lstResults.delete(i)

        sql = "SELECT * FROM methods_comp;"

        rs = self.nametowidget(".").engine.read(True, sql , ())

        if rs:

            for i in rs:
                
                sql = "SELECT test FROM tests WHERE test_id =?;"
                self.test =  self.nametowidget(".").engine.read(False, sql , (i[1],))
                self.y_comp_method = self.get_method_data(i[3])
                self.y_workstation_comp = self.get_workstation_data(i[5])
                self.x_test_method = self.get_method_data(i[2])
                self.x_workstation_test = self.get_workstation_data(i[4])
                data = self.get_method_data(i[2])
                
                if data:
                    if i[7] == 1:
                        if i[6] >= self.correlation_coefficient:
                            tag_config = ("passed",)
                        elif i[6] < self.correlation_coefficient:
                            tag_config = ("not_passed")
                    else:
                        tag_config=()
                        
                   
                    self.lstExperiments.insert("", tk.END, iid=i[0], text=i[0],
                                              values=(data[0],
                                                      data[1],
                                                      data[2],
                                                      self.test,
                                                      self.y_comp_method[3],
                                                      self.y_workstation_comp[0],
                                                      self.x_test_method[3],
                                                      self.x_workstation_test[0],
                                                      i[9].strftime("%d-%m-%Y %H:%M:%S")),
                                               tags=tag_config)

        s = "{0} {1}".format("Experiments", len(self.lstExperiments.get_children()))

        self.experiments.set(s)


    def get_method_data(self, test_method_id):

        sql = "SELECT suppliers.supplier,\
		      wards.ward,\
		      sections.section,\
		      IFNULL(samples.description,'NA') ||' '||IFNULL(methods.method,'NA')||' '||IFNULL(units.unit,'NA')\
	       FROM sites\
	       INNER JOIN suppliers ON sites.comp_id = suppliers.supplier_id\
	       INNER JOIN wards ON sites.site_id = wards.site_id\
	       INNER JOIN sections ON wards.ward_id = sections.ward_id\
	       INNER JOIN tests_methods ON tests_methods.section_id = sections.section_id\
	       INNER JOIN methods_comp ON tests_methods.test_method_id = methods_comp.x_test_method_id\
	       INNER JOIN samples  ON tests_methods.sample_id = samples.sample_id\
	       INNER JOIN methods  ON tests_methods.method_id = methods.method_id\
	       INNER JOIN units ON tests_methods.unit_id = units.unit_id\
               WHERE tests_methods.test_method_id =?;"

        args = (test_method_id,)
        
        return self.nametowidget(".").engine.read(False, sql , args)
        
    def get_workstation_data(self, workstation_id):

        sql = "SELECT workstations.description, workstations.serial FROM workstations WHERE workstation_id =?;"

        args = (workstation_id,)
        
        return self.nametowidget(".").engine.read(False, sql , args)
          
    def on_experiment_selected(self, evt=None):

        if self.lstExperiments.focus():

            item_iid = self.lstExperiments.selection()
            pk = int(item_iid[0])
            self.selected_experiment = self.nametowidget(".").engine.get_selected("methods_comp", "methods_comp_id", pk)
            if self.selected_experiment[7] ==1:
                self.pcc.set(round(self.selected_experiment[6],4))
            else:
                self.pcc.set("")
                
            self.set_results()

    def set_results(self):

        for i in self.lstResults.get_children():
            self.lstResults.delete(i)

        sql = "SELECT * FROM methods_comp_results WHERE methods_comp_id=? ORDER BY recived ASC;"

        args = (self.selected_experiment[0],)
        
        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:
            for i in rs:
                self.lstResults.insert("", tk.END, iid=i[0], text=i[0],
                                       values=(i[2], i[3], i[4].strftime("%d-%m-%Y %H:%M:%S")))

    def on_experiment_activated(self, evt=None):

        if self.lstExperiments.focus():

            item_iid = self.lstExperiments.selection()
            

    def on_result_selected(self, evt=None):

        if self.lstResults.focus():

            item_iid = self.lstResults.selection()

            pk = int(item_iid[0])

            self.selected_result = self.nametowidget(".").engine.get_selected("methods_comp_results", "result_id", pk)
               
    def on_result_activated(self, evt=None):

        if self.lstResults.focus():

            item_iid = self.lstResults.selection()
            obj = frames.methods_comp_result.UI(self, item_iid)
            self.objs.append(obj)
            obj.on_open()

    def on_compute(self, evt=None):

        if self.lstExperiments.focus():

            sql = "SELECT * FROM methods_comp_results WHERE methods_comp_id=?;"

            args = (self.selected_experiment[0],)

            rs = self.nametowidget(".").engine.read(True, sql, args)

            lst_y = []
            lst_x = []

            if rs:
                
                for i in rs:
                    lst_y.append(i[2])
                    lst_x.append(i[3])
                    
                y = np.array(lst_y)
                x = np.array(lst_x)
                n = np.size(x)
                x_mean = np.mean(x)
                y_mean = np.mean(y)

                Sxy = np.sum(x*y)- n*x_mean*y_mean 
                Sxx = np.sum(x*x)-n*x_mean*x_mean 
                  
                slope = Sxy/Sxx 
                intercept = y_mean-slope*x_mean
                slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)

                msg = "The correlation coefficient is: {0}.\nAccept it?".format(round(r,4))
                
                if messagebox.askyesno(self.nametowidget(".").title(), msg, parent=self) == True:

                    sql = "UPDATE methods_comp SET correlation =?, computed =1 WHERE methods_comp_id =?;"
                    args = (r, self.selected_experiment[0],)
                    self.nametowidget(".").engine.write(sql, args)
                    self.set_experiments()
                
    def on_comparisions(self, evt=None):
        if self.lstExperiments.focus():
            frames.comparisions.UI(self).on_open()

    def on_differences(self, evt=None):
        if self.lstExperiments.focus():
            frames.bland_altman.UI(self).on_open()
            
    def on_cancel(self, evt=None):
        for obj in self.objs:
            try:
                obj.destroy()
            except:
                obj.close()
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()

