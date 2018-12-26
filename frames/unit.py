""" This is the unit module of Biovarase."""
import tkinter as tk
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

class Dialog(tk.Toplevel):     
    def __init__(self, parent, engine, index=None):
        super().__init__(name='unit')

        self.resizable(0,0)
        self.transient(parent)
        self.parent = parent
        self.engine = engine
        self.index = index
        self.unit = tk.StringVar()
        self.enable =  tk.BooleanVar()
        self.init_ui()

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        tk.Label(w, text="Unit:").grid(row=0, sticky=tk.W)
        self.txtUnit = tk.Entry(w, bg='white', textvariable=self.unit)
        self.txtUnit.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(w, text="Enable:").grid(row=1, sticky=tk.W)
        tk.Checkbutton(w, onvalue=1, offvalue=0, variable = self.enable,).grid(row=1, column=1,sticky=tk.W)
        
        self.engine.get_save_cancel(self, self)
        
        self.winfo_toplevel().wm_geometry("")

    def on_open(self,selected_item = None):

        if selected_item is not None:
            self.insert_mode = False
            self.selected_item = selected_item
            msg = "Update  unit %s" % (self.selected_item[1],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new unit"
            self.enable.set(1)

        self.title(msg)
        self.txtUnit.focus()

    def set_values(self,):
        
        self.unit.set(self.selected_item[1])
        self.enable.set(self.selected_item[2])        

    def get_values(self,):

        return [self.unit.get(),
                self.enable.get(),]

    def on_save(self, evt):

        if self.engine.on_fields_control( (self.txtUnit,))==False:return

        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.insert_mode == False:

                args.append(self.selected_item[0])

                sql = self.engine.get_update_sql('units', 'unit_id')
                
            
            elif self.insert_mode == True:

                sql = self.engine.get_insert_sql('units', len(args))

                
            self.engine.write(sql, args)
            self.parent.set_values()
            
            if self.index is not None:
                
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)
                
            self.on_cancel()
           
    def on_cancel(self, evt=None):
        self.destroy()
