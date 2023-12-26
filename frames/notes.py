# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import frames.note as ui


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="notes")

        self.parent = parent
        self.attributes('-topmost', True)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.table = "notes"
        self.primary_key = "note_id"
        self.obj = None

        self.test = tk.StringVar()
        self.batch = tk.StringVar()
        self.description = tk.StringVar()
        self.result = tk.StringVar()
        self.recived = tk.StringVar()

        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        f0 = ttk.Frame(self, style="App.TFrame")
        f1 = ttk.Frame(f0, style="App.TFrame", relief=tk.GROOVE, padding=4)
        
        w = ttk.LabelFrame(f1, text='Selected data',)

        ttk.Label(w, text="Test:").pack(side=tk.TOP)
        ttk.Entry(w, textvariable=self.test).pack(side=tk.TOP)
        
        ttk.Label(w, text="Batch:").pack(side=tk.TOP)
        ttk.Entry(w, textvariable=self.batch).pack(side=tk.TOP)

        ttk.Label(w, text="Description:").pack(side=tk.TOP)
        ttk.Entry(w, textvariable=self.description).pack(side=tk.TOP)
        
        ttk.Label(w, text="Result:").pack(side=tk.TOP)
        ttk.Entry(w, textvariable=self.result).pack(side=tk.TOP)
        
        ttk.Label(w, text="Recived:").pack(side=tk.TOP)
        tk.Label(w, font="Verdana 12 bold",
                 textvariable=self.recived).pack(side=tk.TOP)

        w.pack(side=tk.LEFT, fill=tk.Y, expand=0)

        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        f2 = ttk.Frame(f0, style="App.TFrame", relief=tk.GROOVE, padding=4)

        sb = ttk.Scrollbar(f2, orient=tk.VERTICAL)
        self.lstNotes = tk.Listbox(f2, yscrollcommand=sb.set,)
        self.lstNotes.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstNotes.bind("<Double-Button-1>", self.on_item_activated)
        sb.config(command=self.lstNotes.yview)
        self.lstNotes.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)
        
        f3 = ttk.Frame(f0, style="App.TFrame", relief=tk.GROOVE, padding=8)

        bts = (("Add", 0, self.on_add, "<Alt-a>"),
               ("Update", 0, self.on_item_activated, "<Alt-u>"),
               ("Cancel", 0, self.on_cancel, "<Alt-c>"))

        for btn in bts:
            ttk.Button(f3,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])

        f3.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        f2.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=1)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        f0.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        


    def on_open(self, selected_test, selected_batch, selected_result):

        self.selected_test = selected_test
        self.selected_batch = selected_batch
        self.selected_result = selected_result

        self.test.set(selected_test[2])
        self.batch.set(selected_batch[4])
        self.description.set(selected_batch[8])
        self.result.set(round(selected_result[4], 3))

        dt = selected_result[5].strftime('%d-%m-%Y')

        self.recived.set(dt)

        sql = "SELECT notes.note_id,\
                      actions.action,\
                      strftime('%d-%m-%Y', notes.modified),\
                      notes.status\
               FROM notes\
               INNER JOIN actions ON notes.action_id = actions.action_id\
               WHERE result_id =?;"

        args = (selected_result[0],)
        rs = self.nametowidget(".").engine.read(True, sql, args)
        index = 0
        self.dict_items = {}

        if rs:
            self.lstNotes.delete(0, tk.END)
            for i in rs:
                s = '{0}  {1}'.format(i[2], i[1])
                self.lstNotes.insert(tk.END, (s))
                if i[3] != 1:
                    self.lstNotes.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index] = i[0]
                index += 1

        self.title("Notes")

    def on_add(self, evt=None):

        self.obj = ui.UI(self)
        self.obj.on_open(self.selected_test, self.selected_batch, self.selected_result)

    def on_item_activated(self, evt=None):

        if self.lstNotes.curselection():
            index = self.lstNotes.curselection()[0]
            self.obj = ui.UI(self, index)
            self.obj.on_open(self.selected_test,
                             self.selected_batch,
                             self.selected_result,
                             self.selected_note)

        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.nametowidget(".").engine.no_selected,
                                   parent=self)

    def on_item_selected(self, evt=None):

        if self.lstNotes.curselection():
            index = self.lstNotes.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_note = self.nametowidget(".").engine.get_selected(self.table, self.primary_key, pk)

    def on_cancel(self, evt=None):
        """force closing of the child.
        """
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
