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
        super().__init__(name="user")


        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
    
        self.last_name = tk.StringVar()
        self.first_name = tk.StringVar()
        self.nickname = tk.StringVar()
        self.role = tk.IntVar()
        self.elapsing_time = tk.IntVar()
        self.enable_time = tk.BooleanVar()
        self.status = tk.StringVar()
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)


    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame")
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame", padding=4)
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        ttk.Label(frm_left, text="Surname:").grid(row=r, sticky=tk.W)
        self.txLastName = ttk.Entry(frm_left, textvariable=self.last_name)
        self.txLastName.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="First Name:").grid(row=r, sticky=tk.W)
        ent_first_name = ttk.Entry(frm_left, textvariable=self.first_name)
        ent_first_name.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Nick:").grid(row=r, sticky=tk.W)
        ent_nickname = ttk.Entry(frm_left, textvariable=self.nickname)
        ent_nickname.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Level:").grid(row=r, sticky=tk.W)
        spn_role = tk.Spinbox(frm_left, from_=0, to=2, width=5,
                              justify=tk.CENTER,
                              wrap=True,
                              textvariable=self.role)

        spn_role.grid(row=r, column=c,sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Log out time:").grid(row=r, sticky=tk.W)
        spn_elapsing = tk.Spinbox(frm_left, from_=0, to=60, width=5,
                                  justify=tk.CENTER, wrap=True,
                                  textvariable=self.elapsing_time)

        spn_elapsing.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Activate log out:").grid(row=r, sticky=tk.W)
        chk_time = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.enable_time,)
        chk_time.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        chk_status = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status,)
        chk_status.grid(row=r, column=c, sticky=tk.W, **paddings)

        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame", padding=4)
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)

        r = 0
        c = 0
        btn = ttk.Button(frm_buttons, style="App.TButton", text="Save", underline=0, command=self.on_save,)
        self.bind("<Alt-s>", self.on_save)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        btn = ttk.Button(frm_buttons, style="App.TButton", text="Reset", underline=0, command=self.on_reset,)
        self.bind("<Alt-r>", self.on_reset)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        btn = ttk.Button(frm_buttons, style="App.TButton", text="Cancel", underline=0, command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

    def on_open(self):

        if self.index is not None:
            msg = "Update {0}".format(self.winfo_name().title())
            self.set_values()
        else:
            msg = "Insert {0}".format(self.winfo_name().title())
            self.status.set(1)

        self.title(msg)
        self.txLastName.focus()

    def set_values(self,):

        self.last_name.set(self.parent.selected_item[1])
        self.first_name.set(self.parent.selected_item[2])
        self.nickname.set(self.parent.selected_item[3])
        self.role.set(self.parent.selected_item[5])
        self.elapsing_time.set(self.parent.selected_item[6])
        self.enable_time.set(self.parent.selected_item[7])
        self.status.set(self.parent.selected_item[8])

    def get_values(self,):

        if self.index is not None:
            pswrd = self.parent.selected_item[4]
        else:
            pswrd = self.nametowidget(".").engine.get_password("pass")

        return [self.last_name.get(),
                self.first_name.get(),
                self.nickname.get(),
                pswrd,
                self.role.get(),
                self.elapsing_time.get(),
                self.enable_time.get(),
                self.status.get()]

    def on_reset(self, evt=None):

        if self.index is not None:
            pswrd = self.nametowidget(".").engine.get_encript_password("pass")
            sql = "UPDATE users SET pswrd =? WHERE user_id =?;"
            args = (pswrd, self.parent.selected_item[0])
            self.nametowidget(".").engine.write(sql, args)
            msg = "Password reset."
            messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return
        if self.check_nickname() == 0: return
        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.parent.selected_item[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
            self.parent.on_open()

            if self.index is not None:
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)
            else:
                #force focus on listbox
                idx = list(self.parent.dict_items.keys())[list(self.parent.dict_items.values()).index(last_id)]
                self.parent.lstItems.selection_set(idx)
                self.parent.lstItems.see(idx)

            self.on_cancel()

    def check_nickname(self):

        sql = "SELECT user_id, nickname FROM users WHERE nickname =?;"

        rs = self.nametowidget(".").engine.read(False, sql, (self.nickname.get(),))

        if rs:

            if self.index is not None:
                if rs[0] != self.parent.selected_item[0]:
                    msg = "Call sign {0} has already been assigned!".format(self.nickname.get(),)
                    messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
                    return 0
            else:
                msg = "Call sign {0} has already been assigned!".format(self.nickname.get(),)
                messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
                return 0

    def on_cancel(self, evt=None):
        self.destroy()
