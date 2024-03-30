# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="load_tests_sections")

        self.attributes("-topmost", True)
        self.parent = parent
        self.lst_size = tk.IntVar()
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="W.TFrame", padding=8)
        cols = (["#0", 'id', 'w', False, 0, 0],
                ["#1", 'Code', 'w', True, 50, 50],
                ["#2", 'Test', 'w', True, 100, 100],
                ["#3", 'Method', 'w', True, 80, 80],)

        self.lstItems = self.nametowidget(".").engine.get_tree(frm_main, cols)
        self.lstItems.bind("<Double-1>", self.on_item_activated)
        self.lstItems.pack(fill=tk.BOTH, expand=1)
        frm_main.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

    def on_open(self, selected_section):

        self.selected_section = selected_section

        self.set_values()

        msg = "Tests to assign to {0}".format(selected_section[3])
        self.title(msg)

    def set_values(self,):

        for i in self.lstItems.get_children():
            self.lstItems.delete(i)

        sql = "SELECT tests_methods.test_method_id,\
                      tests_methods.code,\
                      tests.description,\
                      methods.method\
               FROM tests\
               INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
               INNER JOIN methods ON tests_methods.method_id = methods.method_id\
               WHERE tests.status=1\
               AND tests_methods.status=1\
               AND tests_methods.section_id !=? OR tests_methods.section_id =0\
               ORDER BY tests.description;"

        args = (self.selected_section[0],)
        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:
            for i in rs:
                self.lstItems.insert('', tk.END, iid=i[0], text=i[0],
                                     values=(i[1], i[2], i[3]),)

    def on_item_activated(self, evt=None):

        if self.lstItems.focus():
            item_iid = self.lstItems.selection()
            pk = int(item_iid[0])
            selected_item = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)

            args = (self.selected_section[0], selected_item[0],)

            sql = "UPDATE tests_methods SET section_id =? WHERE test_method_id =?;"
            self.nametowidget(".").engine.write(sql, args)

            self.set_values()

            args = (self.selected_section[0],)
            self.parent.set_tests_methods(args)

    def on_cancel(self, evt=None):
        self.destroy()
