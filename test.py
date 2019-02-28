""" This is the test module of Biovarase."""
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
        super().__init__(name='test')

        self.attributes('-topmost', True)
        self.resizable(0, 0)
        self.transient(parent) 
        self.parent = parent
        self.engine = kwargs['engine']
        self.index = kwargs['index']

        self.test = tk.StringVar()
        self.cvw = tk.DoubleVar()
        self.cvb = tk.DoubleVar()
        self.enable = tk.BooleanVar()
        self.vcmd = self.engine.get_validate_float(self)
        
        self.engine.center_me(self)
        self.init_ui()

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r = 0
        ttk.Label(w, text="Samples:").grid(row=r, sticky=tk.W)
        self.cbSamples = ttk.Combobox(w)
        self.cbSamples.grid(row=0, column=1, sticky=tk.W)

        r +=1
        ttk.Label(w, text="Units:").grid(row=r, sticky=tk.W)
        self.cbUnits = ttk.Combobox(w)
        self.cbUnits.grid(row=r, column=1, sticky=tk.W)

        r +=1
        ttk.Label(w, text="Test:").grid(row=r, sticky=tk.W)
        self.txTest = ttk.Entry(w, textvariable=self.test)
        self.txTest.grid(row=r, column=1,sticky=tk.W, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Cvw:").grid(row=r, sticky=tk.W)
        self.txtCVW = ttk.Entry(w,
                                width=8,
                                justify=tk.CENTER,
                                validate='key',
                                validatecommand=self.vcmd,
                                textvariable=self.cvw)
        self.txtCVW.grid(row=r, column=1,sticky=tk.W, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Cvb:").grid(row=r, sticky=tk.W)
        self.txtCVB = ttk.Entry(w,
                                width=8,
                                justify=tk.CENTER,
                                validate='key',
                                validatecommand=self.vcmd,
                                textvariable=self.cvb)
        self.txtCVB.grid(row=r, column=1,sticky=tk.W, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        ttk.Checkbutton(w,
                       onvalue=1,
                       offvalue=0,
                       variable=self.enable).grid(row=r,
                                                  column=1,
                                                  sticky=tk.W)

        self.engine.get_save_cancel(self, w)       
    

    def on_open(self, selected_test=None):

        self.set_samples()
        self.set_units()
       
        if self.index is not None:
            self.selected_test = selected_test
            msg = "{0} {1}".format("Update ", self.selected_test[3])
            self.set_values()
        else:
            msg = "Insert new test"
            self.enable.set(1)

        self.title(msg)
        self.txTest.focus()

        
        
    def on_save(self, evt=None):

        if self.engine.on_fields_control(self)==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.engine.get_update_sql('tests', 'test_id')

                args.append(self.selected_test[0])
                       
            else:
                sql = self.engine.get_insert_sql('tests', len(args))

            self.engine.write(sql, args)
            self.parent.on_open()
                
            if self.index is not None:
                self.parent.lstTests.see(self.index)
                self.parent.lstTests.selection_set(self.index)
                    
            self.on_cancel()

    def set_samples(self):

        index = 0
        values = []
        self.dict_samples = {}

        sql = "SELECT sample_id, description FROM samples ORDER BY description ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_samples[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbSamples['values'] = values
        

    def set_units(self):

        index = 0
        values = []
        self.dict_units = {}
        
        sql = "SELECT unit_id, unit FROM units ORDER BY unit ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_units[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbUnits['values'] = values         

    def get_values(self,):
        
        return [self.dict_samples[self.cbSamples.current()],
                self.dict_units[self.cbUnits.current()],
                self.test.get(),
                self.cvw.get(),
                self.cvb.get(),
                self.enable.get()]
    
    def set_values(self,):

        key = next(key for key, 
                   value in self.dict_samples.items() 
                   if value == self.selected_test[1])
        self.cbSamples.current(key)

        key = next(key for key, 
                   value in self.dict_units.items() 
                   if value == self.selected_test[2])
        self.cbUnits.current(key)
        
        self.test.set(self.selected_test[3])
        self.cvw.set(self.selected_test[4])
        self.cvb.set(self.selected_test[5])
        self.enable.set(self.selected_test[6])

    def on_cancel(self, evt=None):
        self.destroy()        
