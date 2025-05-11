# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hashlib

class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="change_password")

        self.parent = parent
        self.transient(parent)
        self.resizable(0, 0)
        self.old_password = tk.StringVar()
        self.new_password = tk.StringVar()
        self.repeat_password = tk.StringVar()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.init_ui()
        self.nametowidget(".").engine.center_window_on_screen(self)
        
    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)
    

        r = 0
        c = 1
        ttk.Label(frm_left, text="Old Password:").grid(row=r, sticky=tk.W)
        self.txtOldPassword = ttk.Entry(frm_left, show='*', textvariable=self.old_password)
        self.txtOldPassword.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="New Password:").grid(row=r, sticky=tk.W)
        self.txtNewPassword = ttk.Entry(frm_left, show='*', textvariable=self.new_password)
        self.txtNewPassword.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="Repet Password:").grid(row=r, sticky=tk.W)
        self.txtRepetPassword = ttk.Entry(frm_left, show='*', textvariable=self.repeat_password)
        self.txtRepetPassword.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

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


    def on_open(self,):

        msg = "Change password."
        self.title(msg)
        self.txtOldPassword.focus()

    def get_values(self,):

        hashed_password = self.nametowidget(".").engine.generate_password(self.new_password.get())

        return (hashed_password.decode('utf-8'),
                self.nametowidget(".").engine.log_user[0])

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            print(self.old_password.get())
            if self.nametowidget(".").engine.check_password(self.old_password.get().encode('utf-8')) == False:
                msg = "Old password is wrong!"
                messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)
            else:

                new_password = self.new_password.get()
                repeat_password = self.repeat_password.get()

                if new_password != repeat_password:
                    msg = "Attention!\nPassword do not match!"
                    messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

                else:
                    args = self.get_values()
                    sql = "UPDATE users SET pswrd =? WHERE user_id =?;"
                    self.nametowidget(".").engine.write(sql, args)
                    self.on_cancel()
        else:
            messagebox.showinfo(self.nametowidget(".").title(), self.nametowidget(".").engine.abort, parent=self)

    def on_cancel(self, evt=None):
        self.destroy()
