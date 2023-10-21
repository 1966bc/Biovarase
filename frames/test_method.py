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
        super().__init__(name="test_method")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        
        self.test = tk.StringVar()
        self.code = tk.StringVar()

        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)
        self.vcmd_int = self.nametowidget(".").engine.get_validate_integer(self)
        self.code.trace("w", lambda x, y, z,
                        c=self.nametowidget(".").engine.get_code_length(),
                        v=self.code: self.nametowidget(".").engine.limit_chars(c, v, x, y, z))
        
        self.is_mandatory = tk.BooleanVar()
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
        ttk.Label(frm_left, text="Code:").grid(row=r, sticky=tk.W)
        self.txCode = ttk.Entry(frm_left, textvariable=self.code)
        self.txCode.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Samples:").grid(row=r, sticky=tk.W)
        self.cbSamples = ttk.Combobox(frm_left,)
        self.cbSamples.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Methods:").grid(row=r, sticky=tk.W)
        self.cbMethods = ttk.Combobox(frm_left,)
        self.cbMethods.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Units:").grid(row=r, sticky=tk.W)
        self.cbUnits = ttk.Combobox(frm_left,)
        self.cbUnits.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Mandatory:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.is_mandatory,)
        chk.grid(row=r, column=c, sticky=tk.EW, **paddings)
                
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

    def on_open(self, selected_test, selected_item=None):

        self.selected_test = selected_test
        self.set_samples()
        self.set_units()
        self.set_methods()
        
        
        if self.index is not None:
            self.selected_item = selected_item
            msg = "Update method for {0} ".format(selected_test[2])
            self.set_values()
        else:
            msg = "Insert method for {0} ".format(selected_test[2])
            self.is_mandatory.set(0)
            self.status.set(1)

        self.title(msg)
        self.txCode.focus()
         
    def set_samples(self):

        index = 0
        self.dict_samples = {}
        voices = []

        sql = "SELECT sample_id, description\
               FROM samples\
               WHERE status =1\
               ORDER BY sample;"

        rs = self.nametowidget(".").engine.read(True, sql)

        x = (0, "Not Assigned")
        rs = (*rs, x)

        for i in rs:
            self.dict_samples[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbSamples["values"] = voices

    def set_units(self):

        index = 0
        self.dict_units = {}
        voices = []

        sql = "SELECT unit_id, unit\
               FROM units\
               WHERE status =1\
               ORDER BY unit"

        rs = self.nametowidget(".").engine.read(True, sql)

        x = (0, "Not Assigned")
        rs = (*rs, x)

        for i in rs:
            self.dict_units[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbUnits["values"] = voices

    def set_methods(self):

        index = 0
        self.dict_methods = {}
        voices = []

        sql = "SELECT method_id, method\
               FROM methods\
               WHERE status =1\
               ORDER BY method"

        rs = self.nametowidget(".").engine.read(True, sql)

        x = (0, "Not Assigned")
        rs = (*rs, x)

        for i in rs:
            self.dict_methods[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbMethods["values"] = voices


    
        
    def set_values(self,):

        self.code.set(self.selected_item[2])
        

        try:
            key = next(key
                       for key, value
                       in self.dict_samples.items()
                       if value == self.selected_item[3])
            self.cbSamples.current(key)
        except:
            pass

        try:
            key = next(key
                       for key, value
                       in self.dict_methods.items()
                       if value == self.selected_item[4])
            self.cbMethods.current(key)
        except:
            pass

        try:
            key = next(key
                       for key, value
                       in self.dict_units.items()
                       if value == self.selected_item[5])
            self.cbUnits.current(key)
        except:
            pass

       
        self.is_mandatory.set(self.selected_item[7])
        self.status.set(self.selected_item[8])


    def get_values(self,):

        if self.index is not None:

            section_id = self.selected_item[7]

        else:
            section_id = 0
            
        return [self.selected_test[0],
                self.code.get(),
                self.dict_samples[self.cbSamples.current()],
                self.dict_methods[self.cbMethods.current()],
                self.dict_units[self.cbUnits.current()],
                section_id,
                self.is_mandatory.get(),
                self.status.get()]
                

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(), self.nametowidget(".").engine.ask_to_save, parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql("tests_methods", "test_method_id")

                args.append(self.selected_item[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql("tests_methods", len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
 
            self.parent.set_test_methods()

            if self.index is not None:
                self.parent.lstTestsMethods.selection_set(self.index)
                self.parent.lstTestsMethods.see(self.index)
                self.parent.lstTestsMethods.focus(self.index)
                
            else:
                self.parent.lstTestsMethods.selection_set(last_id)
                self.parent.lstTestsMethods.see(last_id)
                self.parent.lstTestsMethods.focus(last_id)


            self.on_cancel()

    def on_cancel(self, evt=None):
        self.destroy()
