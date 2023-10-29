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
        super().__init__(name="ward")

        if self.nametowidget(".").engine.get_instance("data"):
                self.nametowidget(".data").on_cancel()     

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        self.ward = tk.StringVar()
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
        ttk.Label(frm_left, text="Hospital:").grid(row=r, sticky=tk.W)
        self.cbSites = ttk.Combobox(frm_left,)
        self.cbSites.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Manager:").grid(row=r, sticky=tk.W)
        self.cbUsers = ttk.Combobox(frm_left,)
        self.cbUsers.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Ward:").grid(row=r, sticky=tk.W)
        self.txtWard = ttk.Entry(frm_left, textvariable=self.ward)
        self.txtWard.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status,)
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

    def on_open(self, selected_hospital):

        self.selected_hospital = selected_hospital
        self.set_sites()
        self.set_manager()

        if self.index is not None:
            msg = "Update {0}".format(self.winfo_name().title())
            self.set_values()
            self.txtWard.focus()
        else:
            msg = "Insert {0}".format(self.winfo_name().title())

            try:
                key = next(key
                           for key, value
                           in self.dict_sites.items()
                           if value == selected_hospital[0])
                self.cbSites.current(key)

                self.cbUsers.focus()
                
            except:
                pass
        
            self.status.set(1)

        self.title(msg)
        
    def set_sites(self):

        index = 0
        self.dict_sites = {}
        voices = []

        sql = "SELECT sites.site_id, suppliers.supplier\
               FROM sites\
               INNER JOIN suppliers ON sites.comp_id = suppliers.supplier_id\
               ORDER BY suppliers.supplier;"
    
        rs = self.nametowidget(".").engine.read(True, sql, ())

        for i in rs:
            self.dict_sites[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbSites["values"] = voices

    def set_manager(self):

        index = 0
        self.dict_users = {}
        voices = []

        sql = "SELECT user_id, last_name||' '||first_name\
               FROM users\
               WHERE status =1\
               ORDER BY last_name;"

        rs = self.nametowidget(".").engine.read(True, sql)

        for i in rs:
            self.dict_users[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbUsers["values"] = voices        

    def set_values(self,):

        try:
            key = next(key
                       for key, value
                       in self.dict_sites.items()
                       if value == self.parent.selected_ward[1])
            self.cbSites.current(key)
        except:
            pass


        try:
            key = next(key
                       for key, value
                       in self.dict_users.items()
                       if value == self.parent.selected_ward[2])
            self.cbUsers.current(key)
        except:
            pass
        
        self.ward.set(self.parent.selected_ward[3])
        self.status.set(self.parent.selected_ward[4])

    def get_values(self,):

        return [self.dict_sites[self.cbSites.current()],
                self.dict_users[self.cbUsers.current()],
                self.ward.get(),
                self.status.get()]
    
    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.parent.selected_ward[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
            self.parent.set_wards((self.parent.selected_hospital[0],))

            if self.nametowidget(".").engine.get_instance("sections"):
                self.nametowidget(".sections").set_values()

            if self.index is not None:
                self.parent.lstWards.see(self.index)
                self.parent.lstWards.selection_set(self.index)
                
            self.on_cancel()

        else:
            messagebox.showinfo(self.nametowidget(".").title(),
                                self.nametowidget(".").engine.abort,
                                parent=self)

    def on_cancel(self, evt=None):
        self.destroy()
