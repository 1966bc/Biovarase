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
__date__ = "2018-12-25"
__status__ = "Production"


class Dialog(tk.Toplevel):     
    def __init__(self, parent, engine):
        super().__init__(name='rejections')

        self.transient(parent) 
        self.resizable(0, 0)
        self.parent = parent
        self.engine = engine
        
        self.test = tk.StringVar()
        self.batch = tk.StringVar()
        self.result = tk.StringVar()
        self.recived = tk.StringVar()
        self.obj = None

        self.init_ui()
        self.engine.center_me(self)

    def init_ui(self):
    
        f0 = self.engine.get_frame(self)

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

        w = self.engine.get_frame(f0)

        self.lstItems = self.engine.get_listbox(w, width=40)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        
        w.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand =1)

        self.engine.get_add_edit_cancel(self,f0)

        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self, selected_test, selected_batch, selected_result):

        self.selected_test = selected_test 
        self.selected_batch = selected_batch 
        self.selected_result = selected_result

        self.test.set(selected_test[1])
        self.batch.set(selected_batch[2])
        self.result.set(selected_result[2])

        dt = selected_result[3].strftime('%Y-%m-%d')
        
        self.recived.set(dt)

        sql = "SELECT * FROM lst_rejections WHERE result_id =?"
        args = (selected_result[0],)
        rs = self.engine.read(True, sql, args)

        index = 0

        self.dict_items={}

        if rs:
            self.lstItems.delete(0, tk.END)
            for i in rs:
                s = '{:20}{:20}'.format(i[3],i[1])
                self.lstItems.insert(tk.END, (s))
                if i[4] != 1:
                    self.lstItems.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index]=i[0]
                index+=1
                
        self.title("Rejections")

    def on_add(self, evt):

        self.obj = frames.rejection.Dialog(self,self.engine)
        self.obj.on_open(self.selected_test,self.selected_batch, self.selected_result)

    def on_edit(self, evt):
        self.on_item_activated(self)
        

    def on_item_activated(self,evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            self.obj = frames.rejection.Dialog(self,self.engine, index)
            self.obj.transient(self)
            self.obj.on_open(self.selected_test,
                             self.selected_batch,
                             self.selected_result,
                             self.selected_item)
               
        else:
            messagebox.showwarning(self.engine.title,self.engine.no_selected)
  
    def on_item_selected(self, evt):

         if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.engine.get_selected('rejections','rejection_id', pk)
            
    
    def on_cancel(self, evt=None):

        """force closing of the childs...
        """     
        
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
    
