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
import frames.test as ui


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="tests")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.attributes("-topmost", True)
        self.table = "tests"
        self.primary_key = "test_id"
        self.obj = None
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")
        
        frm_left = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        self.lblTests = tk.LabelFrame(frm_left, text="Tests")
        
        cols = (["#0", 'test_id', 'w', False, 0, 0],
                ["#1", 'Test', 'w', True, 200, 200],
                ["#2", 'Specialities', 'w', True, 100, 100],)

        self.lstItems = self.nametowidget(".").engine.get_tree(frm_left, cols)
        self.lstItems.tag_configure('status', background=self.nametowidget(".").engine.get_rgb(211, 211, 211))
        self.lstItems.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-1>", self.on_item_activated)

        frm_buttons = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        bts = (("Add", 0, self.on_add, "<Alt-a>"),
               ("Update", 0, self.on_item_activated, "<Alt-u>"),
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
        frm_buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)

    def on_open(self,):
        msg = "{0} Management".format(self.winfo_name().capitalize())
        self.title(msg)
        self.set_values()

    def set_values(self):

        for i in self.lstItems.get_children():
            self.lstItems.delete(i)


        sql = "SELECT tests.test_id,\
                      tests.test,\
                      specialities.description,\
                      tests.status\
               FROM tests\
               INNER JOIN specialities ON tests.speciality_id = specialities.speciality_id\
               ORDER BY tests.test ASC;"

        rs = self.nametowidget(".").engine.read(True, sql, ())

        if rs:

            for i in rs:

                if i[3] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("",)

                self.lstItems.insert('', tk.END, iid=i[0], text=i[0],
                                     values=(i[1], i[2], ),
                                     tags=tag_config)

        s = "{0} {1}".format("Tests", len(self.lstItems.get_children()))
        self.lblTests["text"] = s
           

    def on_add(self, evt=None):

        self.obj = ui.UI(self,)
        self.obj.on_open()

    def on_item_selected(self, evt=None):

          if self.lstItems.focus():
            item_iid = self.lstItems.selection()
            pk = int(item_iid[0])
            self.selected_item = self.nametowidget(".").engine.get_selected(self.table,
                                                                            self.primary_key,
                                                                            pk)        

    def on_item_activated(self, evt=None):

        if self.lstItems.focus():
            item_iid = self.lstItems.selection()
            self.obj = ui.UI(self, item_iid)
            self.obj.on_open(self.selected_item,)

        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.nametowidget(".").engine.no_selected,
                                   parent=self)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
