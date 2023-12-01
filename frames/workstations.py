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
import frames.workstation as ui


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name='workstations')

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.table = "workstations"
        self.primary_key = "workstation_id"
        self.obj = None
        self.init_ui()
        self.center_me()

    def center_me(self,):
        """center window on the screen"""

        x = self.parent.winfo_rootx()
        y = self.parent.winfo_rooty()
        self.geometry("+%d+%d" % (x, y))           

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

        w = tk.LabelFrame(frm_right, text='Workstations')
        cols = (["#0", 'id', 'w', False, 0, 0],
                ["#1", 'Equipments', 'w', True, 200, 200],
                ["#2", 'Workstations', 'w', True, 200, 200],
                ["#3", 'Serial', 'w', True, 100, 100],
                ["#4", 'Device ID', 'w', True, 200, 200],)

        self.lstWorkstations = self.nametowidget(".").engine.get_tree(frm_right, cols)
        self.lstWorkstations.tag_configure('status', background=self.nametowidget(".").engine.get_rgb(211, 211, 211))
        self.lstWorkstations.bind("<<TreeviewSelect>>", self.on_workstation_selected)
        self.lstWorkstations.bind("<Double-1>", self.on_workstation_activated)

        w.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm_main.pack(fill=tk.BOTH, expand=1)
        frm_left.pack(side=tk.LEFT, fill=tk.Y,expand=0)
        frm_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def on_open(self,):

        msg = "{0} Management".format(self.winfo_name().capitalize())
        self.title(msg)
        self.set_values()
            
    def on_reset(self):

        for i in self.lstWorkstations.get_children():
            self.lstWorkstations.delete(i)

    def set_values(self):

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

        for i in rs:
            
            sites = self.Sites.insert("", i[0], text=i[1], values=(i[0], "sites"))
            rs_labs = self.load_labs(i[0])

            if rs_labs is not None:

                for lab in rs_labs:
                    labs = self.Sites.insert(sites, lab[0], text=lab[1], values=(lab[0], "labs"))
                    rs_sections = self.load_sections(lab[0])
                    
                    if rs_sections is not None:
                        
                        for section in rs_sections:
                            self.Sites.insert(labs, section[0], text=section[1], values=(section[0], "sections"))

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

                self.set_workstations(args)

            else:
                self.on_reset()

           
    def on_branch_activated(self, evt=None):

        s = self.Sites.focus()
        d = self.Sites.item(s)

        if d["values"]:

            if d["values"][1] == "sections":

                pk = d["values"][0]

                self.selected_section = self.nametowidget(".").engine.get_selected("sections", "section_id", pk)

                self.obj = ui.UI(self,)

                self.obj.on_open(self.selected_section)


    def set_workstations(self, args):

        for i in self.lstWorkstations.get_children():
            self.lstWorkstations.delete(i)

        sql = "SELECT workstations.workstation_id,\
                      equipments.description,\
                      workstations.description,\
                      workstations.serial,\
                      workstations.device_id,\
                      workstations.status\
               FROM workstations\
               INNER JOIN equipments ON workstations.equipment_id = equipments.equipment_id\
               INNER JOIN sections ON workstations.section_id = sections.section_id\
               WHERE sections.section_id =?\
               AND equipments.status =1;"

        rs = self.nametowidget(".").engine.read(True, sql, args)
    
        if rs:
            
            for i in rs:

                if i[5] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("",)       


                self.lstWorkstations.insert('', tk.END, iid=i[0], text=i[0],
                                            values=(i[1], i[2], i[3], i[4], i[5]),
                                            tags=tag_config)
                
        
    def on_workstation_selected(self, evt=None):

        if self.lstWorkstations.focus():
            item_iid = self.lstWorkstations.selection()
            pk = int(item_iid[0])
            self.selected_workstation = self.nametowidget(".").engine.get_selected( self.table, self.primary_key,  pk)

    def on_workstation_activated(self, evt=None):

        if self.lstWorkstations.focus():
            item_iid = self.lstWorkstations.selection()
            pk = int(item_iid[0])
            selected_workstation = self.nametowidget(".").engine.get_selected( self.table, self.primary_key, pk)
            self.obj = ui.UI(self, item_iid)
            self.obj.on_open(self.selected_section, selected_workstation,)

        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.nametowidget(".").engine.no_selected,
                                   parent=self)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()

