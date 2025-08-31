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
from calendarium import Calendarium


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="note")

        self.parent = parent
        self.index = index
        self.attributes('-topmost', True)
        self.transient(parent)
        self.resizable(0, 0)

        self.description = tk.StringVar()
        self.status = tk.BooleanVar()
        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)

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
        ttk.Label(frm_left, text="Actions:").grid(row=r, sticky=tk.W)
        self.cbActions = ttk.Combobox(frm_left,)
        self.cbActions.grid(row=r, column=1, sticky=tk.W)

        r += 1
        ttk.Label(frm_left, text="Description:").grid(row=r, sticky=tk.W)
        self.txDescription = ttk.Entry(frm_left, textvariable=self.description,)
        self.txDescription.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        self.modified = Calendarium(frm_left, "Modified")
        self.modified.get_calendarium(frm_left, r, 1)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status,)
        chk.grid(row=r, column=1, sticky=tk.W)

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

    def on_open(self, selected_test, selected_batch,
                selected_result, selected_note=None):

        self.selected_test = selected_test
        self.selected_batch = selected_batch
        self.selected_result = selected_result

        self.set_actions()

        if self.index is not None:
            msg = "Update {0}".format(self.winfo_name().title())
            self.set_values()
        else:
            msg = "Add {0}".format(self.winfo_name().title())
            self.status.set(1)
            self.modified.set_today()

        self.title(msg)
        self.cbActions.focus()

    def set_actions(self):

        sql = "SELECT action_id, action FROM actions WHERE status =1 ORDER BY action ASC;"
        rs = self.nametowidget(".").engine.read(True, sql, ())
        index = 0
        self.dict_actions = {}
        voices = []

        for i in rs:
            self.dict_actions[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbActions['values'] = voices

    def set_values(self,):

        key = next(key
                   for key, value
                   in self.dict_actions.items()
                   if value == self.parent.selected_note[2])
        self.cbActions.current(key)

        self.description.set(self.parent.selected_note[3])

        self.modified.year.set(int(self.parent.selected_note[4][0:4]))
        self.modified.month.set(int(self.parent.selected_note[4][5:7]))
        self.modified.day.set(int(self.parent.selected_note[4][8:10]))

        self.status.set(self.parent.selected_note[5])

    def get_values(self,):

        return [self.selected_result[0],
                self.dict_actions[self.cbActions.current()],
                self.description.get(),
                self.modified.get_date(self),
                self.status.get()]        

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return
        if self.modified.get_date(self) == False: return
        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.build_sql(self.parent.table, op="update")
                args.append(self.parent.selected_note[0])

            else:

                sql = self.nametowidget(".").engine.build_sql(self.parent.table, op="insert")

            self.nametowidget(".").engine.write(sql, args)
            self.parent.on_open(self.selected_test,
                                self.selected_batch,
                                self.selected_result)

            if self.index is not None:
                self.parent.lstNotes.see(self.index)
                self.parent.lstNotes.selection_set(self.index)

            self.on_cancel()

    def on_cancel(self, evt=None):
        self.destroy()

    
