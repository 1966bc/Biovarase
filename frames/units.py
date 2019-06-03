""" This is the units module of Biovarase."""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frames.unit as unit

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"

class Widget(tk.Toplevel):     
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='units')

        self.parent = parent
        self.engine = kwargs['engine']
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        self.attributes('-topmost', True)
        self.objs = []
        self.init_ui()
        self.engine.center_me(self)

    def init_ui(self):
    
        f0 = self.engine.get_frame(self,8)
        f1 = ttk.Frame(f0,)
        self.lstItems = self.engine.get_listbox(f1,)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        self.engine.get_add_edit_cancel(self, f0)
        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
    def on_open(self,):
        self.title('Units')
        self.set_values()
        
    def set_values(self):

        self.lstItems.delete(0, tk.END)
        index = 0
        self.dict_items = {}
        sql = "SELECT * FROM units"
        rs = self.engine.read(True, sql, ())
        
        if rs:
            for i in rs:
                self.lstItems.insert(tk.END, i[1])
                if i[2] != 1:
                    self.lstItems.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index] = i[0]
                index += 1

    def on_add(self, evt):

        obj = unit.Widget(self, engine=self.engine,index =None)
        obj.on_open()
        self.objs.append(obj)

    def on_edit(self, evt):
        self.on_item_activated()
        
    def on_item_activated(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            obj = unit.Widget(self, engine=self.engine, index=index)
            obj.on_open(self.selected_item,)
            self.objs.append(obj)
               
        else:
            messagebox.showwarning(self.engine.title, self.engine.no_selected, parent=self)
      
    def on_item_selected(self, evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.engine.get_selected('units', 'unit_id', pk)

    def on_cancel(self, evt=None):
        for obj in self.objs:
            obj.destroy()
        self.destroy()
    
