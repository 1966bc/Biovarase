""" This is the batch module of Biovarase."""
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
        super().__init__(name='batch')  

        self.resizable(0, 0)
        self.transient(parent) 
        self.parent = parent
        self.engine = engine
        self.index = index
        self.day =  tk.IntVar()
        self.month =  tk.IntVar()
        self.year =  tk.IntVar()

        self.batch = tk.StringVar()
        self.target = tk.DoubleVar()
        self.sd = tk.DoubleVar()
        self.enable =  tk.BooleanVar()

        self.vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%tk.W')

        self.init_ui()

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r = 0
        tk.Label(w, text="Batch:").grid(row=r, sticky=tk.W)
        self.txtBatch = tk.Entry(w, bg='white', textvariable=self.batch)
        self.txtBatch.grid(row=r, column=1, padx=5, pady=5)

        r = 1
        tk.Label(w, text="Expiration:").grid(row=r,column=0,sticky=tk.W)

        self.engine.get_calendar(self,w,r)

        r = 2
        tk.Label(w, text="Target:").grid(row=r, sticky=tk.W)
        self.txtTarget = tk.Entry(w,
                               bg='white',
                               validate = 'key',
                               validatecommand = self.vcmd,
                               textvariable=self.target)
        self.txtTarget.grid(row=r, column=1, padx=5, pady=5)

        r = 3
        tk.Label(w, text="SD:").grid(row=r, sticky=tk.W)
        self.txtSD = tk.Entry(w,
                           bg='white',
                           validate = 'key',
                           validatecommand = self.vcmd,
                           textvariable=self.sd)
        self.txtSD.grid(row=r, column=1, padx=5, pady=5)

        r = 4
        tk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        tk.Checkbutton(w,
                       onvalue=1,
                       offvalue=0,
                       variable=self.enable).grid(row=r,
                                                  column=1,
                                                  sticky=tk.W)

        self.engine.get_save_cancel(self, self) 
        

    def on_open(self, selected_test, selected_batch = None):

        self.selected_test = selected_test

        if self.index is not None:
            self.selected_batch = selected_batch
            msg = "{0} {1}".format("Update ", self.selected_batch[2])
            self.set_values()
        else:
            msg = "{0} {1}".format("Insert new batch for ", selected_test[1])
            self.engine.set_calendar_date(self)
            self.enable.set(1)

        self.title(msg)
        self.txtBatch.focus()
        
    def on_save(self, evt=None):

        fields =  (self.txtBatch, self.txtTarget, self.txtSD)
        
        if self.engine.on_fields_control(fields)==False:return
        if self.engine.get_calendar_date(self)==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.index is not None:

                sql = self.engine.get_update_sql('batchs','batch_id')

                args.append(self.selected_batch[0])
                       
            else:

                sql = self.engine.get_insert_sql('batchs',len(args))

            self.engine.write(sql,args)
            self.parent.set_batches()
            
            if self.index is not None:
                self.parent.lstBatches.see(self.index)
                self.parent.lstBatches.selection_set(self.index)
                    
            self.on_cancel()

        else:
            messagebox.showinfo(self.engine.title,self.engine.abort)
               
            
    def on_cancel(self, evt=None):
        self.destroy()

    def get_values(self,):

        return [self.selected_test[0],
                self.batch.get(),
                self.engine.get_calendar_date(self,),
                self.target.get(),
                self.sd.get(),
                self.enable.get()]
    
    def set_values(self,):

        self.year.set(int(self.selected_batch[3][0:4]))
        self.month.set(int(self.selected_batch[3][5:7]))
        self.day.set(int(self.selected_batch[3][8:10]))
        self.batch.set(self.selected_batch[2])
        self.target.set(self.selected_batch[4])
        self.sd.set(self.selected_batch[5])
        self.enable.set(self.selected_batch[6])
      

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type,
                 trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            if text:
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True          
