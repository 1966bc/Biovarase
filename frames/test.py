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
        self.test = tk.StringVar()
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
        ttk.Label(frm_left, text="Specialities:").grid(row=r, sticky=tk.W)
        self.cbSpecialities = ttk.Combobox(frm_left,)
        self.cbSpecialities.grid(row=r, column=c, sticky=tk.EW, **paddings)
        
        r += 1
        ttk.Label(frm_left, text="Test:").grid(row=r, sticky=tk.W)
        self.txTest = ttk.Entry(frm_left, textvariable=self.test)
        self.txTest.grid(row=r, column=c, sticky=tk.EW, **paddings)

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


    def on_open(self, selected_item=None):

        self.set_specialities()

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Update {0}".format(self.winfo_name().capitalize())
            self.set_values()
        else:
            msg = "Insert {0}".format(self.winfo_name().capitalize())
            self.status.set(1)

        self.title(msg)
        self.cbSpecialities.focus()

    def set_specialities(self):

        index = 0
        self.dict_specialities = {}
        voices = []

        sql = "SELECT speciality_id, description\
               FROM specialities\
               WHERE status =1\
               ORDER BY description"

        rs = self.nametowidget(".").engine.read(True, sql)

        x = (0, "Not Assigned")
        rs = (*rs, x)

        for i in rs:
            self.dict_specialities[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbSpecialities["values"] = voices
        
    def get_values(self,):

        return [self.dict_specialities[self.cbSpecialities.current()],
                self.test.get(),
                self.status.get(),]

    def set_values(self,):

        try:
            key = next(key
                       for key, value
                       in self.dict_specialities.items()
                       if value == self.selected_item[1])
            self.cbSpecialities.current(key)
        except:
            pass

        self.test.set(self.selected_item[2])
        self.status.set(self.selected_item[3])

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

            self.parent.lstItems.focus()
            
            if self.index is not None:
                idx = self.index
            else:
                idx = last_id
                
            self.parent.lstItems.see(idx)
            self.parent.lstItems.selection_set(idx)
            self.on_cancel()
            
    def update_tests_methods(self, last_id):

        if self.nametowidget(".").engine.get_instance("tests_methods") == True:

            self.nametowidget(".tests_methods").set_tests()

            if last_id != 0:
                which = last_id
            else:
                which = self.selected_item[0]
            #print(which)
            idx = list(self.nametowidget(".tests_methods").dict_tests.keys())[list(self.nametowidget(".tests_methods").dict_tests.values()).index(which)]
            #print(idx)
            self.nametowidget(".tests_methods").lstTests.see(idx) 
            self.nametowidget(".tests_methods").lstTests.selection_set(idx)
            self.nametowidget(".tests_methods").lstTests.event_generate("<<ListboxSelect>>")
            
    def on_cancel(self, evt=None):
        self.destroy()
