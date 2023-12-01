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
        super().__init__(name="section")

        if self.nametowidget(".").engine.get_instance("data"):
                self.nametowidget(".data").on_cancel()     
        
        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)

        self.section = tk.StringVar()
        self.status = tk.BooleanVar()
        self.set_it = tk.BooleanVar()
        
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
        ttk.Label(frm_left, text="Labs:").grid(row=r, sticky=tk.W)
        self.cbWards = ttk.Combobox(frm_left,)
        self.cbWards.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Managers:").grid(row=r, sticky=tk.W)
        self.cbUsers = ttk.Combobox(frm_left,)
        self.cbUsers.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Field:").grid(row=r, sticky=tk.W)
        self.txSection = ttk.Entry(frm_left, textvariable=self.section)
        self.txSection.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status,)
        chk.grid(row=r, column=c, sticky=tk.EW, **paddings)

        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)
        
        r = 0
        c = 0
        btn = ttk.Button(frm_buttons, style="App.TButton", text="Save", underline=0, command=self.on_save,)
        self.bind("<Alt-s>", self.on_save)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)
  
        r += 1
        btn = ttk.Button(frm_buttons, style="App.TButton", text="Cancel", underline=0, command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r +=1 
        ttk.Checkbutton(frm_buttons,
                        text = "Set It",
                        onvalue=1,
                        offvalue=0,
                        variable=self.set_it,).grid(row=r,
                                                    column=c,
                                                    sticky=tk.W)


    def on_open(self, selected_lab, selected_section=None):

        self.selected_lab = selected_lab
        self.set_wards()
        self.set_employees()
        self.set_ward(selected_lab)

        if self.index is not None:
            self.selected_section = selected_section
            msg = "Update Medical Field"
            self.set_values()
        else:
            msg = "Insert Medical Field"
            self.status.set(1)

        self.title(msg)
        self.cbWards.focus()

    def set_wards(self):

        index = 0
        self.dict_labs = {}
        values = []

        sql = "SELECT lab_id, lab\
               FROM labs WHERE site_id =? AND status =1 ORDER BY lab ASC;"
        args = (self.selected_lab[1],)
        rs = self.nametowidget(".").engine.read(True, sql, args)

        for i in rs:
            self.dict_labs[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbWards['values'] = values

    def set_ward(self, selected_lab):
        try:
            key = next(key for key, value
                       in self.dict_labs.items()
                       if value == selected_lab[0])
            self.cbWards.current(key)
        except:
            pass
    
    def set_employees(self):
        
        index = 0
        self.dict_users = {}
        values = []

        sql = "SELECT user_id, last_name||' '||first_name FROM users WHERE status =1 ORDER BY last_name;"
        rs = self.nametowidget(".").engine.read(True, sql, ())
       
        for i in rs:
            self.dict_users[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbUsers['values'] = values


    def get_values(self,):

        return [self.dict_labs[self.cbWards.current()],
                self.dict_users[self.cbUsers.current()],
                self.section.get(),
                self.status.get()]

    def set_values(self,):

        try:
            key = next(key for key, value
                       in self.dict_labs.items()
                       if value == self.selected_section[1])
            self.cbWards.current(key)
        except:
            pass

        try:
            key = next(key for key, value
                       in self.dict_users.items()
                       if value == self.selected_section[2])
            self.cbUsers.current(key)
        except:
            pass

        self.section.set(self.selected_section[3])
        self.status.set(self.selected_section[4])

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(), self.nametowidget(".").engine.ask_to_save, parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.selected_section[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))


            last_id = self.nametowidget(".").engine.write(sql, args)      

            args = (self.selected_lab[0],)

            self.parent.set_sections(args)

            if self.index is not None:

                if self.set_it.get():
                    self.nametowidget(".").engine.set_section_id(self.selected_section[0])
                try:
                    self.parent.lstSections.focus(self.index)
                    self.parent.lstSections.selection_set(self.index)
                except:
                    pass
            else:
                try:
                    if self.set_it.get():
                        self.nametowidget(".").engine.set_section_id(last_id)
                    self.parent.lstSections.focus(last_id)
                    self.parent.lstSections.selection_set(last_id)
                except:
                    pass

            self.reset_main()
            self.on_cancel()

    def reset_main(self,):

        self.nametowidget(".main").on_open()
        self.nametowidget(".main").on_reset()

    def on_cancel(self, evt=None):
        self.destroy()
