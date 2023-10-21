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
        self.table = "sections"
        self.primary_key = "section_id"
        self.obj = None
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

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
        
        self.lblSections = tk.LabelFrame(frm_right, text="Sections")
        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Manager", 'w', True, 200, 200],
                ["#2", "Section", 'w', True, 200, 200],)

        self.lstSections = self.nametowidget(".").engine.get_tree(self.lblSections, cols)
        self.lstSections.tag_configure('status', background=self.nametowidget(".").engine.get_rgb(211, 211, 211))
        self.lstSections.bind("<<TreeviewSelect>>", self.on_section_selected)
        self.lstSections.bind("<Double-1>", self.on_section_activated)

        self.lblSections.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm_main.pack(fill=tk.BOTH, expand=1)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        frm_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
    def on_open(self,):

        msg = "{0} Management".format(self.winfo_name().capitalize())
        self.title(msg)

        sql = "SELECT sites.site_id,suppliers.supplier AS site\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id"

        rs = self.nametowidget(".").engine.read(True, sql, ())

        if rs:
            self.set_values(rs)
            
    def on_reset(self):

        for i in self.lstSections.get_children():
            self.lstSections.delete(i)

    def set_values(self, rs):

        #.insert(parent, index, iid=None, **kw)
        self.Sites.insert("", 0, 0, text="Sites")

        for i in rs:
            #print(i)
            sites = self.Sites.insert("",
                                      i[0],
                                      text=i[1],
                                      values=(i[0], "sites"))
            rs_wards = self.load_wards(i[0])

            if rs_wards is not None:

                for ward in rs_wards:
                    
                    wards = self.Sites.insert(sites,
                                              ward[0],
                                              text=ward[1],
                                              values=(ward[0], "wards"))
 
    def load_wards(self, i):

        sql = "SELECT ward_id, ward\
               FROM wards\
               WHERE site_id =?\
               AND status =1"

        return self.nametowidget(".").engine.read(True, sql, (i,))


    def on_branch_selected(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "wards":

                pk = d["values"][0]

                self.selected_ward = self.nametowidget(".").engine.get_selected("wards", "ward_id", pk)

                args = (self.selected_ward[0],)

                self.set_sections(args)

            else:
                self.on_reset()

           
    def on_branch_activated(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "wards":

                pk = d["values"][0]

                self.selected_ward = self.nametowidget(".").engine.get_selected("wards", "ward_id", pk)

                self.obj = ui.UI(self,)

                self.obj.on_open(self.selected_ward)


    def set_sections(self, args):

        for i in self.lstSections.get_children():
            self.lstSections.delete(i)

        sql = "SELECT sections.section_id,\
                      users.last_name ||' '|| users.first_name,\
                      sections.section,\
                      sections.status,\
                      wards.ward_id\
               FROM sections\
               INNER JOIN users ON sections.user_id = users.user_id\
               INNER JOIN wards ON sections.ward_id = wards.ward_id\
               WHERE wards.ward_id = ?\
               AND wards.status =1"

        rs = self.nametowidget(".").engine.read(True, sql, args)
    
        if rs:
            
            for i in rs:

                if i[3] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("",)       


                self.lstSections.insert('', tk.END, iid=i[0], text=i[0],
                                            values=(i[1], i[2], i[3]),
                                            tags=tag_config)
                
        s = "{0} {1}".format("Sections", len(self.lstSections.get_children()))                
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
            self.obj.on_open(self.selected_ward, selected_section,)

        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.nametowidget(".").engine.no_selected,
                                   parent=self)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()

