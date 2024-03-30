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


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="test")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        
        self.description = tk.StringVar()
        self.status = tk.BooleanVar()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        
        ttk.Label(frm_left, text="Description:").grid(row=r, sticky=tk.W)
        self.txDescription = ttk.Entry(frm_left, textvariable=self.description)
        self.txDescription.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status)
        chk.grid(row=r, column=c, sticky=tk.EW, **paddings)

        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)
        
        r = 0
        c = 0
        btn_save = ttk.Button(frm_buttons, style="App.TButton", text="Save", underline=0, command=self.on_save,)
        self.bind("<Alt-s>", self.on_save)
        btn_save.grid(row=r, column=c, sticky=tk.EW, **paddings)
  
        r += 1
        btn_cancel = ttk.Button(frm_buttons, style="App.TButton", text="Cancel", underline=0, command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn_cancel.grid(row=r, column=c, sticky=tk.EW, **paddings)


    def on_open(self):

        if self.index is not None:
            msg = "Update {0}".format(self.winfo_name().capitalize())
            self.selected_item = self.parent.selected_item
            self.set_values()
        else:
            msg = "Insert {0}".format(self.winfo_name().title())
            self.status.set(1)

        self.title(msg)
        self.txDescription.focus()

    def get_values(self,):

        return [self.description.get(),
                self.status.get(),]

    def set_values(self,):

        self.description.set(self.selected_item[1])
        self.status.set(self.selected_item[2])

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(), self.nametowidget(".").engine.ask_to_save, parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.selected_item[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
            self.parent.set_values()
            self.update_tests_methods(last_id)
            self.select_item(last_id)
            self.on_cancel()

    def select_item(self, last_id=None):

        #searches for the key using the primary key of the record
        if self.index is not None:
            lst_index = [k for k,v in self.parent.dict_items.items() if v == self.selected_item[0]]
        else:
            lst_index = [k for k,v in self.parent.dict_items.items() if v == last_id]

        # point the right item on listbox
        self.parent.lstItems.see(lst_index[0])
        self.parent.lstItems.selection_set(lst_index[0])
        self.parent.on_item_selected()

    def update_tests_methods(self, last_id):

        if self.nametowidget(".").engine.get_instance("tests_methods") == True:

            self.nametowidget(".tests_methods").set_tests()

            if self.index is not None:
                which = self.selected_item[0]
            else:
                which = last_id

            point_to = list(self.nametowidget(".tests_methods").dict_tests.keys())[list(self.nametowidget(".tests_methods").dict_tests.values()).index(which)]

            self.nametowidget(".tests_methods").lstTests.focus()        
            self.nametowidget(".tests_methods").lstTests.see(point_to) 
            self.nametowidget(".tests_methods").lstTests.selection_set(point_to)
            self.nametowidget(".tests_methods").lstTests.event_generate("<<ListboxSelect>>")
            
    def on_cancel(self, evt=None):
        self.destroy()
