# -*- coding: utf-8 -*-
""" This is the rejections module of Biovarase."""
import tkinter as tk
from tkinter import messagebox
import frames.rejection

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2021-03-14"
__status__ = "Production"


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="rejections")

        self.parent = parent
        self.attributes('-topmost', True)
        self.transient(parent)
        self.resizable(0, 0)

        self.test = tk.StringVar()
        self.batch = tk.StringVar()
        self.result = tk.StringVar()
        self.recived = tk.StringVar()
        self.obj = None

        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        f0 = self.nametowidget(".").engine.get_frame(self)

        w = tk.LabelFrame(f0, text='Select data',)

        tk.Label(w, text="Test:").pack(side=tk.TOP)
        tk.Label(w,
                 font = "Verdana 12 bold",
                 textvariable = self.test).pack(side=tk.TOP)

        tk.Label(w, text="Batch:").pack(side=tk.TOP)
        tk.Label(w,
                 font = "Verdana 12 bold",
                 textvariable = self.batch).pack(side=tk.TOP)

        tk.Label(w, text="Result:").pack(side=tk.TOP)
        tk.Label(w,
                 font = "Verdana 12 bold",
                 textvariable = self.result).pack(side=tk.TOP)

        tk.Label(w, text="Recived:").pack(side=tk.TOP)
        tk.Label(w,
                 font = "Verdana 12 bold",
                 textvariable = self.recived).pack(side=tk.TOP)

        w.pack(side=tk.LEFT, fill=tk.Y, expand=0)

        w = self.nametowidget(".").engine.get_frame(f0)

        self.lstItems = self.nametowidget(".").engine.get_listbox(w, width=40)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)

        w.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand =1)

        self.nametowidget(".").engine.get_add_edit_cancel(self,f0)

        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self, selected_test, selected_batch, selected_result):

        self.selected_test = selected_test
        self.selected_batch = selected_batch
        self.selected_result = selected_result

        self.set_values()

        self.title("Rejections")

    def set_values(self):

        self.lstItems.delete(0, tk.END)

        self.test.set(self.selected_test[1])
        self.batch.set(self.selected_batch[2])
        self.result.set(self.selected_result[2])
        dt = self.selected_result[3].strftime('%Y-%m-%d')
        self.recived.set(dt)

        index = 0
        self.dict_items = {}
        args = (self.selected_result[0],)
        sql = "SELECT * FROM lst_rejections WHERE result_id =?"
        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:
            for i in rs:
                s = '{:20}{:20}'.format(i[3],i[1])
                self.lstItems.insert(tk.END, (s))
                if i[4] != 1:
                    self.lstItems.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index]=i[0]
                index+=1

    def on_add(self, evt):

        self.obj = frames.rejection.UI(self)
        self.obj.on_open(self.selected_test,self.selected_batch, self.selected_result)

    def on_edit(self, evt):
        self.on_item_activated(self)

    def on_item_activated(self,evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            self.obj = frames.rejection.UI(self, index)
            self.obj.on_open(self.selected_test,
                             self.selected_batch,
                             self.selected_result,
                             self.selected_item)

        else:
            messagebox.showwarning(self.master.title(),self.nametowidget(".").engine.no_selected, parent = self)

    def on_item_selected(self, evt):

         if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.nametowidget(".").engine.get_selected('rejections','rejection_id', pk)


    def on_cancel(self, evt=None):

        """force closing of the childs...
        """

        if self.obj is not None:
            self.obj.destroy()
        self.destroy()

