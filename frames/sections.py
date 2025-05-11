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
import frames.section as ui


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="sections")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.attributes("-topmost", True)
        self.table = "sections"
        self.primary_key = "section_id"
        self.obj = None
        self.init_ui()
        self.nametowidget(".").engine.center_window_on_screen(self)
        self.nametowidget(".").engine.set_instance(self, 1)

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
        
        self.lblSections = tk.LabelFrame(frm_right, text="Medical Fields")
        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Lab", 'w', True, 0, 200],
                ["#2", "Section", 'w', True, 0, 200],
                ["#3", "Manager", 'w', True, 0, 100],)

        self.lstSections = self.nametowidget(".").engine.get_tree(self.lblSections, cols)
        self.lstSections.tag_configure('status', background=self.nametowidget(".").engine.get_rgb(211, 211, 211))
        self.lstSections.bind("<<TreeviewSelect>>", self.on_section_selected)
        self.lstSections.bind("<Double-1>", self.on_section_activated)

        self.lblSections.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm_main.pack(fill=tk.BOTH, expand=1)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        frm_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
    def on_open(self,):

        msg = "Medical Fields Management"
        self.title(msg)
        self.set_values()

    def set_values(self):

        for i in self.Sites.get_children():
            self.Sites.delete(i)

        for i in self.lstSections.get_children():
            self.lstSections.delete(i)

        sql = "SELECT DISTINCT(sites.supplier_id),suppliers.description\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.supplier_id\
               WHERE sites.status =1\
               GROUP BY sites.supplier_id\
               ORDER BY suppliers.description;"

        rs = self.nametowidget(".").engine.read(True, sql, ())

        #.insert(parent, index, iid=None, **kw)
        self.Sites.insert("", 0, 0, text="Laboratories")

        for i in rs:
            sites = self.Sites.insert("", i[0], text=i[1], values=(i[0], "sites"))
            rs_hospitals = self.load_hospitals(i[0])

            if rs_hospitals is not None:
                for hospital in rs_hospitals:
                    hospitals = self.Sites.insert(sites, hospital[0], text=hospital[1], values=(hospital[0], "hospitals"))
                    rs_labs = self.load_labs(hospital[0])

                    if rs_labs is not None:
                        for lab in rs_labs:
                            self.Sites.insert(hospitals, lab[0], text=lab[1], values=(lab[0], "labs"))

    def load_hospitals(self, i):

        sql = "SELECT sites.site_id,suppliers.description\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id\
               WHERE sites.supplier_id =?\
               AND sites.status =1;"

        return self.nametowidget(".").engine.read(True, sql, (i,))                    
 
    def load_labs(self, i):

        sql = "SELECT lab_id, lab\
               FROM labs\
               WHERE site_id =?\
               AND status =1"

        return self.nametowidget(".").engine.read(True, sql, (i,))

    def on_branch_selected(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "labs":

                pk = d["values"][0]

                self.selected_lab = self.nametowidget(".").engine.get_selected("labs", "lab_id", pk)

                args = (self.selected_lab[0],)

                self.set_sections(args)

    def on_branch_activated(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "labs":

                pk = d["values"][0]

                self.selected_lab = self.nametowidget(".").engine.get_selected("labs", "lab_id", pk)

                self.obj = ui.UI(self,)

                self.obj.on_open(self.selected_lab)


    def set_sections(self, args):

        for i in self.lstSections.get_children():
            self.lstSections.delete(i)

        sql = "SELECT sections.section_id,\
                      labs.lab,\
                      sections.section,\
                      users.last_name ||' '|| users.first_name,\
                      sections.status,\
                      labs.lab_id\
               FROM sections\
               INNER JOIN users ON sections.user_id = users.user_id\
               INNER JOIN labs ON sections.lab_id = labs.lab_id\
               WHERE labs.lab_id = ?\
               AND labs.status =1"

        rs = self.nametowidget(".").engine.read(True, sql, args)
    
        if rs:
            
            for i in rs:

                if i[4] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("",)       


                self.lstSections.insert('', tk.END, iid=i[0], text=i[0],
                                            values=(i[1], i[2], i[3], i[4]),
                                            tags=tag_config)
                
        s = "{0} {1}".format("Medical Fields", len(self.lstSections.get_children()))                
        self.lblSections["text"] = s       
        
    def on_section_selected(self, evt=None):

        if self.lstSections.focus():
            item_iid = self.lstSections.selection()
            pk = int(item_iid[0])
            self.selected_section = self.nametowidget(".").engine.get_selected( self.table, self.primary_key,  pk)

    def on_section_activated(self, evt=None):

        if self.lstSections.focus():
            item_iid = self.lstSections.selection()
            pk = int(item_iid[0])
            selected_section = self.nametowidget(".").engine.get_selected( self.table, self.primary_key, pk)
            self.obj = ui.UI(self, item_iid)
            self.obj.on_open(self.selected_lab, selected_section,)

        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.nametowidget(".").engine.no_selected,
                                   parent=self)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()

