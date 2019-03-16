""" This is the tests module of Biovarase."""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frames.test

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
        super().__init__(name='tests')

        self.parent = parent
        self.engine = kwargs['engine']
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        self.attributes('-topmost', True)
        
        self.obj = None
        
        self.init_ui()
        self.engine.center_me(self)
        
    def init_ui(self):
    
        f0 = self.engine.get_frame(self, 8)
        
        w = ttk.Frame(f0,)
        self.lstTests = self.engine.get_listbox(w,)
        self.lstTests.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstTests.bind("<Double-Button-1>", self.on_item_activated)
        w.pack(side=tk.LEFT, fill=tk.BOTH,padx=5, pady=5, expand =1)
        
        self.engine.get_add_edit_cancel(self,f0)
        
        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self,):
        self.title("Tests")
        self.set_values()
        
    def set_values(self):

        self.lstTests.delete(0, tk.END)
        index = 0
        self.dict_items = {}

        sql = "SELECT tests.test_id,tests.test||' '||samples.sample, tests.enable\
               FROM tests\
               INNER JOIN samples ON tests.sample_id = samples.sample_id\
               ORDER BY tests.test"
        
        rs = self.engine.read(True, sql, ())

        if rs:
            for i in rs:
                s = "{:}".format(i[1])
                self.lstTests.insert(tk.END, s)
                if i[2] != 1:
                    self.lstTests.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index] = i[0]
                index += 1
        

    def on_add(self, evt):

        self.obj = frames.test.Dialog(self, engine=self.engine, index=None)
        self.obj.on_open()

    def on_edit(self, evt):
        self.on_item_activated()
        
    def on_item_activated(self, evt=None):

        if self.lstTests.curselection():
            index = self.lstTests.curselection()[0]
            self.obj = frames.test.Dialog(self, engine=self.engine, index=index)
            self.obj.on_open(self.selected_test,)
               
        else:
            messagebox.showwarning(self.engine.title,self.engine.no_selected, parent=self)
                
    def on_item_selected(self, evt):

        if self.lstTests.curselection():
            index = self.lstTests.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_test = self.engine.get_selected('tests','test_id', pk)
            

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
    
