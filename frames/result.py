""" This is the result module of Biovarase."""
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
    def __init__(self,parent, engine, index=None):
        super().__init__(name='result')  

        self.resizable(0, 0)
        self.transient(parent) 
        self.parent = parent
        self.engine = engine
        self.index = index
        self.day =  tk.IntVar()
        self.month =  tk.IntVar()
        self.year =  tk.IntVar()
        self.test = tk.StringVar()
        self.batch = tk.StringVar()
        self.result = tk.DoubleVar()
        self.enable =  tk.BooleanVar()
        self.vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%tk.W')

        self.init_ui()

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r = 0
        tk.Label(w, text="Test:").grid(row=r, sticky=tk.W)
        tk.Label(w,
                 font = "Verdana 12 bold",
                 textvariable = self.test).grid(row=r,
                                                column=1,
                                                sticky=tk.W,
                                                padx=5, pady=5)

        r = 1
        tk.Label(w, text="Batch:").grid(row=r, sticky=tk.W)
        tk.Label(w,
                 font = "Verdana 12 bold",
                 textvariable = self.batch).grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r = 2
        tk.Label(w, text="Result:").grid(row=r, sticky=tk.W)
        self.txtResult = tk.Entry(w,
                                  width=8,
                                  bg='white',
                                  validate = 'key',
                                  validatecommand = self.vcmd,
                                  textvariable=self.result)
        self.txtResult.grid(row=r, column=1,sticky=tk.W, padx=5, pady=5)

        r = 3
        tk.Label(w, text="Recived:").grid(row=r, column=0, sticky=tk.W)

        self.engine.get_calendar(self, w, r)

        r = 4
        tk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        tk.Checkbutton(w,
                       onvalue=1,
                       offvalue=0,
                       variable = self.enable,).grid(row=r,
                                                     column=1,
                                                     sticky=tk.W)

        if self.index is not None:
            self.engine.get_save_cancel_delete(self, self)
        else:
            self.engine.get_save_cancel(self, self)


    def on_open(self, selected_test, selected_batch, selected_result=None):

        self.selected_batch = selected_batch
        self.test.set(selected_test[1])
        self.batch.set(self.selected_batch[2])

        if self.index is not None:
            self.selected_result = selected_result
            msg = "Update"
            self.set_values()
        else:
            msg = "Add"
            self.enable.set(1)
            self.engine.set_calendar_date(self)

        self.title(msg)
        self.txtResult.focus()
        
    def on_save(self, evt=None):

        fields = (self.txtResult,)
        if self.engine.on_fields_control( fields)==False:return
        if self.engine.get_calendar_date(self)==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.index is not None:
                sql = self.engine.get_update_sql('results','result_id')
                args.append(self.selected_result[0])
    
            else:
                sql = self.engine.get_insert_sql('results',len(args))
      
            self.engine.write(sql,args)
            self.parent.set_results()
                
            if self.index is not None:
                self.parent.lstResults.see(self.index)
                self.parent.lstResults.selection_set(self.index)
                    
            self.on_cancel()
    
    def on_cancel(self, evt=None):
        self.destroy()

    def on_delete(self, evt=None):

        if self.index is not None:
            if messagebox.askyesno(self.engine.title, self.engine.delete, parent=self) == True:
                sql = "DELETE FROM results WHERE result_id =?"
                args = (self.selected_result[0],)
                self.engine.write(sql,args)
                self.parent.set_results()
                self.on_cancel()  
            else:
                messagebox.showinfo(self.engine.title,self.engine.abort)

    def get_values(self,):

        return [self.selected_batch[0],
                self.result.get(),
                self.engine.get_calendar_timestamp(self),
                self.enable.get()]
       
    def set_values(self,):

        try:
            self.year.set(int(self.selected_result[3].year))
            self.month.set(int(self.selected_result[3].month))
            self.day.set(int(self.selected_result[3].day))
        except:
            pass

        self.result.set(self.selected_result[2])
        self.enable.set(self.selected_result[4])

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
         
