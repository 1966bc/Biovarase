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
import frames.test_method as ui
import frames.goal as goal

SQL = "SELECT tests_methods.test_method_id,\
              tests_methods.code,\
              samples.description,\
              methods.method,\
              units.unit,\
              tests_methods.status\
       FROM tests\
       INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
       INNER JOIN samples ON tests_methods.sample_id = samples.sample_id\
       INNER JOIN methods ON tests_methods.method_id = methods.method_id\
       INNER JOIN units ON tests_methods.unit_id = units.unit_id\
       WHERE tests.test_id =?\
       AND tests.status=1\
       ORDER BY tests.test;"

class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="tests_methods")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.attributes("-topmost", True)
        self.obj = None
        self.items = tk.StringVar()
        self.init_ui()
        self.nametowidget(".").engine.set_me_center(self)
        self.nametowidget(".").engine.set_instance(self, 1)
            
    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")

        frm_left = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)
        ttk.Label(frm_left, style='App.TLabel', textvariable=self.items,).pack(fill=tk.X, expand=0)
        sb = ttk.Scrollbar(frm_left, orient=tk.VERTICAL)
        self.lstTests = tk.Listbox(frm_left, yscrollcommand=sb.set,)
        self.lstTests.bind("<<ListboxSelect>>", self.on_test_selected)
        self.lstTests.bind("<Double-Button-1>", self.on_test_activated)
        sb.config(command=self.lstTests.yview)
        self.lstTests.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)
        

        frm_right = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Code", "w", True, 50, 50],
                ["#2", "Sample", "w", True, 50, 50],
                ["#3", "Method", "w", True, 80, 80],
                ["#4", "Unit", "w", True, 80, 80],)

        self.lstTestsMethods = self.nametowidget(".").engine.get_tree(frm_right, cols,)
        self.lstTestsMethods.tag_configure("status", background="light gray")
        self.lstTestsMethods.bind("<Double-1>", self.on_test_method_activated)

        frm_buttons = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        bts = (("Goals", 0, self.on_analytical_goal, "<Alt-b>"),
               ("Cancel", 0, self.on_cancel, "<Alt-c>"))

        for btn in bts:
            ttk.Button(frm_buttons,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])

        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_right.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        
    def on_analytical_goal(self, evt=None):
        
        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
            self.obj = goal.UI(self, item_iid)
            self.obj.on_open(selected_test_method)
            
    def on_open(self,):

        msg = "Test Methods Management"
        self.title(msg)
        self.set_tests()

    def set_tests(self, evt=None):

        self.lstTests.delete(0, tk.END)
        index = 0
        self.dict_tests = {}

        sql = "SELECT * FROM tests WHERE status =1 ORDER BY test ASC;"
        
        rs = self.nametowidget(".").engine.read(True, sql, ())

        if rs:
            for i in rs:
                s = "{0}".format(i[2])
                self.lstTests.insert(tk.END, s)
                self.dict_tests[index] = i[0]
                index += 1
                
        msg = ("Tests: {0}".format(self.lstTests.size()))
        self.items.set(msg)

    def set_test_methods(self):

        for i in self.lstTestsMethods.get_children():
            self.lstTestsMethods.delete(i)

        args = (self.selected_test[0],)
        
        rs = self.nametowidget(".").engine.read(True, SQL, args)

        if rs:
            for i in rs:
                if i[5] != 1:
                    tag_config = ("status",)    
                else:
                    tag_config = ("",)            

                self.lstTestsMethods.insert("", tk.END, iid=i[0], text=i[0],
                                            values=(i[1], i[2], i[3], i[4]),
                                            tags = tag_config)
                
    def on_test_selected(self, evt):

        if self.lstTests.curselection():
            index = self.lstTests.curselection()[0]
            pk = self.dict_tests.get(index)
            self.selected_test = self.nametowidget(".").engine.get_selected("tests", "test_id", pk)
            self.set_test_methods()

    def on_test_activated(self, evt):

        if self.lstTests.curselection():
            index = self.lstTests.curselection()[0]
            self.obj = ui.UI(self)
            self.obj.on_open(self.selected_test)
            
    def on_test_method_activated(self, evt):

        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            selected_item = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
            self.obj = ui.UI(self, item_iid)
            self.obj.on_open(self.selected_test, selected_item,)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()
