""" This is the action rejection of Biovarase."""
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

class Dialog(tk.Toplevel):     
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='rejection')

        self.attributes('-topmost', True)
        self.resizable(0,0)
        self.transient(parent) 
        self.parent = parent
        self.engine = kwargs['engine']
        self.index = kwargs['index']
        
        self.day =  tk.IntVar()
        self.month =  tk.IntVar()
        self.year =  tk.IntVar()
        self.description = tk.StringVar()
        self.enable =  tk.BooleanVar()
        
        self.engine.center_me(self)
        self.init_ui()

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r =0       
        tk.Label(w, text="Actions:").grid(row=r, sticky=tk.W)
        self.cbActions = ttk.Combobox(w,)
        self.cbActions.grid(row=r, column=1, sticky=tk.W,padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Description:").grid(row=r, sticky=tk.W)
        self.txDescription = ttk.Entry(w, textvariable=self.description,)
        self.txDescription.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Modified:").grid(row=r, column=0, sticky=tk.W)
        self.engine.get_calendar(self, w, r,1)

        r +=1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        ttk.Checkbutton(w,
                       onvalue=1,
                       offvalue=0,
                       variable = self.enable).grid(row=r,
                                                    column=1,
                                                    sticky=tk.W)

        if self.index is not None:
            self.engine.get_save_cancel_delete(self, w)
        else:
            self.engine.get_save_cancel(self, w)

    def on_open(self, selected_test, selected_batch, selected_result, selected_rejection = None):

        self.selected_test = selected_test
        self.selected_batch = selected_batch
        self.selected_result = selected_result

        self.set_actions()
          
        if self.index is not None:
            self.selected_rejection = selected_rejection
            msg = "Update rejection"
            self.set_values()
        else:
            msg = "Add rejection"
            self.enable.set(1)
            self.engine.set_calendar_date(self)

        self.title(msg)
        self.cbActions.focus()
        
    def on_save(self, evt=None):
        
        if self.engine.on_fields_control(self)==False:return
        if self.engine.get_calendar_date(self)==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.index is not None:

                sql = self.engine.get_update_sql('rejections','rejection_id')

                args = (*args, self.selected_rejection[0])
                       
            else:
                sql = self.engine.get_insert_sql('rejections',len(args))

            self.engine.write(sql,args)
            self.parent.on_open(self.selected_test,self.selected_batch,self.selected_result)

            if self.index is not None:
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)
                
            self.on_cancel()

    def on_delete(self, evt=None):

        if self.index is not None:
            if messagebox.askyesno(self.engine.title, self.engine.delete, parent=self) == True:
        
                sql = "DELETE FROM rejections WHERE rejection_id =?"
                args = (self.selected_rejection[0],)
                self.engine.write(sql,args)
                self.parent.on_open(self.selected_test,self.selected_batch,self.selected_result)

                if self.index is not None:
                    self.parent.lstItems.see(self.index)
                    self.parent.lstItems.selection_set(self.index)

                self.on_cancel()
    
            else:
                messagebox.showinfo(self.engine.title,self.engine.abort, parent=self)
        
    def set_actions(self):

        index = 0
        values = []
        self.dict_actions = {}
        
        sql = "SELECT action_id, action FROM actions ORDER BY action ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_actions[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbActions['values'] = values
 

    def get_values(self,):

        return (self.selected_result[0],
                self.dict_actions[self.cbActions.current()],
                self.description.get(),
                self.engine.get_calendar_timestamp(self),
                self.enable.get())
    
    def set_values(self,):

        key = next(key for key, value in self.dict_actions.items() if value == self.selected_rejection[2])
        self.cbActions.current(key)

        self.description.set(self.selected_rejection[3])

        self.year.set(int(self.selected_rejection[4].year))
        self.month.set(int(self.selected_rejection[4].month))
        self.day.set(int(self.selected_rejection[4].day))
      
        self.enable.set(self.selected_rejection[5])

    def on_cancel(self, evt=None):
        self.destroy()
