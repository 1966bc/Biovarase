""" This is the actions module of Biovarase."""
import tkinter as tk
from tkinter import messagebox
import frames.action as action

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"

class Dialog(tk.Toplevel):     
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='actions')

        self.attributes('-topmost', True)
        self.parent = parent
        self.engine = kwargs['engine']
        self.obj = None
        self.engine.center_me(self)
        self.init_ui()

    def init_ui(self):
    
        f0 = self.engine.get_frame(self)

        f1 = tk.Frame(f0,)
        self.lstActions = self.engine.get_listbox(f1,)
        self.lstActions.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstActions.bind("<Double-Button-1>", self.on_item_activated)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        self.engine.get_add_edit_cancel(self,f0)

        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self,):
               
        self.title("Correttive Actions")
        self.set_values()

    def set_values(self):

        self.lstActions.delete(0, tk.END)
        index = 0
        self.dict_items = {}
        sql = "SELECT * FROM actions"
        rs = self.engine.read(True, sql, ())

        if rs:
            for i in rs:
                self.lstActions.insert(tk.END, i[1])
                if i[2] != 1:
                    self.lstActions.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index] = i[0]
                index += 1

    def on_add(self, evt):

        self.obj = action.Dialog(self, engine=self.engine, index=None)
        self.obj.on_open()

    def on_edit(self, evt):
        self.on_item_activated()
        
    def on_item_activated(self, evt=None):

        if self.lstActions.curselection():
            index = self.lstActions.curselection()[0]
            self.obj = action.Dialog(self, engine=self.engine, index=index)
            self.obj.on_open(self.selected_item,)
               
        else:
            messagebox.showwarning(self.engine.title,self.engine.no_selected, parent=self)
                
    def on_item_selected(self, evt):

        if self.lstActions.curselection():
            index = self.lstActions.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.engine.get_selected('actions','action_id', pk)
            
    def on_cancel(self, evt=None):

        """force closing of the childs...
        """     
        
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
    
