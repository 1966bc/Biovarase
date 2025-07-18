# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk

import frames.load_tests_sections as ui


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="tests_sections")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(800, 600)
        self.obj = None
        self.table = "tests"
        self.primary_key = "test_id"
        self.init_ui()
        self.nametowidget(".").engine.center_window_on_screen(self)
        
    def init_ui(self):
        
        frm_main = ttk.Frame(self, style="App.TFrame")
        frm_sites = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        cols = (["#0", "", "w", False, 300, 300],
                ["#1", "", "w", False, 0, 0],)
        self.Sites = self.nametowidget(".").engine.get_tree(frm_sites, cols, show="tree")
        self.Sites.show = "tree"
        self.Sites.pack(fill=tk.BOTH, padx=2, pady=2)
        self.Sites.bind("<<TreeviewSelect>>", self.on_branch_selected)
        self.Sites.bind("<Double-1>", self.on_branch_activated)
        
        frm_lists = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        self.lblDictTests = ttk.LabelFrame(frm_lists, style="App.TLabelframe", text="Tests:")
        
        cols = (["#0", 'id', 'w', False, 0, 0],
                ["#1", 'Code', 'w', True, 80, 80],
                ["#2", 'Test', 'w', True, 200, 200],
                ["#3", 'Method', 'w', True, 80, 80],)

        self.lstItems = self.nametowidget(".").engine.get_tree(self.lblDictTests, cols)
        self.lstItems.tag_configure("status", background="light gray")
        self.lstItems.bind("<<TreeviewSelect>>", self.on_selected_dict_test)
        self.lstItems.bind("<Double-1>", self.on_activated_dict_test)
        self.lstItems.pack(fill=tk.BOTH, expand=1)

        self.lblDictTests.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    
        frm_sites.pack(side=tk.LEFT, fill=tk.Y,padx=5, pady=5,expand=0)
        frm_lists.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5,expand=1)
        
        frm_main.pack(fill=tk.BOTH, expand=1)

        
    def on_open(self,):

        self.title("Tests Labs")
        self.set_values()
    
    def set_values(self):

        sql = "SELECT sites.site_id,suppliers.description AS site\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id\
               WHERE sites.status=1;"

        rs = self.nametowidget(".").engine.read(True, sql, ())

        #.insert(parent, index, iid=None, **kw)
        self.Sites.insert("", 0, 0, text="Sites")

        if rs:

            for i in rs:
                
                sites = self.Sites.insert("", i[0], text=i[1], values=(i[0], "sites"))
                rs_labs = self.load_labs(i[0])

                if rs_labs is not None:

                    for lab in rs_labs:
                        
                        labs = self.Sites.insert(sites, lab[0], text=lab[1], values=(lab[0], "labs"))

                        rs_sections = self.load_sections(lab[0])

                        if rs_sections is not None:
                            
                            for section in rs_sections:
                                self.Sites.insert(labs, section[0], text=section[1],
                                                  values=(section[0], "sections"))
                    
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

    def on_branch_selected(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "sections":

                pk = d["values"][0]

                self.selected_section = self.nametowidget(".").engine.get_selected("sections", "section_id", pk)

                args = (self.selected_section[0],)

                self.set_tests_methods(args)

           
    def on_branch_activated(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "sections":

                pk = d["values"][0]

                selected_section = self.nametowidget(".").engine.get_selected("sections", "section_id", pk)

                self.obj = ui.UI(self)
                self.obj.on_open(selected_section)
            
    def set_tests_methods(self, args):

        for i in self.lstItems.get_children():
            self.lstItems.delete(i)

        sql = "SELECT dict_tests.dict_test_id,\
                      dict_tests.code,\
                      tests.description,\
                      methods.method,\
                      dict_tests.status\
               FROM tests\
               INNER JOIN dict_tests ON tests.test_id = dict_tests.test_id\
               INNER JOIN methods ON dict_tests.method_id = methods.method_id\
               WHERE dict_tests.section_id =?\
               AND tests.status=1\
               AND dict_tests.status=1\
               ORDER BY tests.description;"
    
        rs = self.nametowidget(".").engine.read(True, sql, args)
    
        if rs:
            
            for i in rs:

                if i[4] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("")          

                self.lstItems.insert('', tk.END, iid=i[0], text=i[0],
                                            values=(i[1], i[2], i[3]),
                                            tags = tag_config)

        s = "{0} {1}".format("Tests", len(self.lstItems.get_children()))

        self.lblDictTests["text"] = s                

    def on_selected_dict_test(self, evt=None):

        if self.lstItems.focus():

            item_iid = self.lstItems.selection()

            pk = int(item_iid[0])
            
            self.selected_dict_test = self.nametowidget(".").engine.get_selected("dict_tests", "dict_test_id", pk)
            self.selected_test = self.nametowidget(".").engine.get_selected("tests", "test_id", self.selected_dict_test[1])
            
    def on_activated_dict_test(self, evt=None):

        if self.lstItems.focus():

            item_iid = self.lstItems.selection()

            pk = int(item_iid[0])

            selected_item = self.nametowidget(".").engine.get_selected("dict_tests", "dict_test_id", pk)

            sql = "UPDATE dict_tests SET section_id = 0 WHERE dict_test_id =?;"
            args = (selected_item[0],)
            self.nametowidget(".").engine.write(sql, args)
            args = (self.selected_section[0],)
            self.set_tests_methods(args)
            try:
                if self.obj.winfo_exists():
                    self.obj.set_values()
            except:
                pass

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
