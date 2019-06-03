""" This is the action module of Biovarase."""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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
        super().__init__(name='action')

        self.parent = parent
        self.engine = kwargs['engine']
        self.index = kwargs['index']
        self.resizable(0, 0)
        self.transient(parent) 
        self.unit = tk.StringVar()
        self.enable =  tk.BooleanVar()
        self.init_ui()
        self.engine.center_me(self)

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r =0
        ttk.Label(w, text="Action:").grid(row=r, sticky=tk.W)
        self.txtAction = ttk.Entry(w, textvariable=self.unit)
        self.txtAction.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        ttk.Checkbutton(w,
                       onvalue=1,
                       offvalue=0,
                       variable = self.enable,).grid(row=r,
                                                     column=1,
                                                     sticky=tk.W)

        self.engine.get_save_cancel(self, w) 

    def on_open(self,selected_item = None):

        if self.index is not None:
            self.selected_item = selected_item
            msg = "{0} {1}".format("Update ", self.selected_item[1])
            self.set_values()
        else:
            msg = "Insert new action"
            self.enable.set(1)

        self.title(msg)
        self.txtAction.focus()

    def set_values(self,):
        
        self.unit.set(self.selected_item[1])
        self.enable.set(self.selected_item[2])        

    def get_values(self,):

        return (self.unit.get(),
                self.enable.get(),)

    def on_save(self, evt):

        if self.engine.on_fields_control(self)==False:return

        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.index is not None:

                sql = self.engine.get_update_sql('actions','action_id')

                args = (*args, self.selected_item[0])
   
            else:
                sql = self.engine.get_insert_sql('actions',len(args))

            self.engine.write(sql,args)
            self.parent.set_values()
            
            if self.index is not None:
                self.parent.lstActions.see(self.index)
                self.parent.lstActions.selection_set(self.index)
                
            self.on_cancel()

        else:
            messagebox.showinfo(self.engine.title, self.engine.abort, parent=self)
           
    def on_cancel(self, evt=None):
        self.destroy()
