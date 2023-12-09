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

import frames.unit as ui

SQL = "SELECT unit_id, unit, status FROM units ORDER BY unit;"

class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="units")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.table = "units"
        self.field = "unit_id"
        self.obj = None
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")
        frm_left = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        sb = ttk.Scrollbar(frm_left, orient=tk.VERTICAL)
        self.lstItems = tk.Listbox(frm_left, yscrollcommand=sb.set,)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        sb.config(command=self.lstItems.yview)
        self.lstItems.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)

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

        frm_buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)

    def on_open(self,):

        msg = "{0} Management".format(self.winfo_name().title())
        self.title(msg)
        self.set_values()

    def set_values(self):

        self.lstItems.delete(0, tk.END)
        index = 0
        self.dict_items = {}
        
        rs = self.nametowidget(".").engine.read(True, SQL, ())

        if rs:
            self.lstItems.delete(0, tk.END)

            for i in rs:
                s = "{:}".format(i[1])
                self.lstItems.insert(tk.END, s)
                if i[2] != 1:
                    self.lstItems.itemconfig(index, {"bg":"light gray"})
                self.dict_items[index] = i[0]
                index += 1

    def on_add(self, evt=None):

        self.obj = ui.UI(self,)
        self.obj.on_open()
        
    def on_edit(self, evt):
        self.on_item_activated()

    def on_item_selected(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.nametowidget(".").engine.get_selected(self.table,
                                                                            self.field,
                                                                            pk)

    def on_item_activated(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            self.obj = ui.UI(self, index)
            self.obj.on_open()

        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.nametowidget(".").engine.no_selected,
                                   parent=self)            

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
