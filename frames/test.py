#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018                                                        
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox

class Dialog(Toplevel):     
    def __init__(self,parent, engine, index = None):
        super().__init__(name='test')
        
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.index = index
        self.grid() 

        self.test = StringVar()
        self.cvw = DoubleVar()
        self.cvb = DoubleVar()
        self.enable =  BooleanVar()
        self.vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.center_me()
        self.init_ui()

    def center_me(self):
        
        """center window on the screen"""
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2
        self.geometry("+%d+%d" % (x, y))

    def cols_configure(self,w):
        
        w.columnconfigure(0, weight=1)
        w.columnconfigure(1, weight=1)
        w.columnconfigure(2, weight=1)                

    def init_ui(self):

        w = self.engine.get_frame(self)        
        self.cols_configure(w)
        w.grid(row = 0, column = 0, sticky=N+W+S+E)

        Label(w, text="Samples:").grid(row=0, sticky=W)
        self.cbSamples = ttk.Combobox(w,)
        self.cbSamples.grid(row=0, column=1)

        Label(w, text="Units:").grid(row=1, sticky=W)
        self.cbUnits = ttk.Combobox(w,)
        self.cbUnits.grid(row=1, column=1)

        Label(w, text="Test:").grid(row=2, sticky=W)
        self.txTest = Entry(w, bg='white', textvariable=self.test)
        self.txTest.grid(row=2, column=1, padx=5, pady=5)

        Label(w, text="Cvw:").grid(row=3, sticky=W)
        self.txtCVW = Entry(w,
                            bg='white',
                            validate = 'key',
                            validatecommand = self.vcmd,
                            textvariable=self.cvw)
        self.txtCVW.grid(row=3, column=1, padx=5, pady=5)

        Label(w, text="Cvb:").grid(row=4, sticky=W)
        self.txtCVB = Entry(w,
                            bg='white',
                            validate = 'key',
                            validatecommand = self.vcmd,
                            textvariable=self.cvb)
        self.txtCVB.grid(row=4, column=1, padx=5, pady=5)

        Label(w, text="Enable:").grid(row=5, sticky=W)
        Checkbutton(w, onvalue=1, offvalue=0, variable = self.enable,).grid(row=5, column=1,sticky=W)

        self.engine.get_save_cancel(self, self)

    def on_open(self,selected_test = None):

        self.set_samples()
        self.set_units()
       
        if self.index is not None:
            self.selected_test = selected_test
            msg = "Update  %s" % (self.selected_test[3],)
            self.set_values()
        else:
            msg = "Insert new test"
            self.enable.set(1)

        self.title(msg)
        self.txTest.focus()
        
    def on_save(self, evt=None):

        fields = (self.cbSamples, self.txTest, self.txtCVW, self.txtCVB)
        
        if self.engine.on_fields_control(fields)==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.index is not None:

                sql = self.engine.get_update_sql('tests','test_id')

                args.append(self.selected_test[0])
                       
            else:
                sql = self.engine.get_insert_sql('tests',len(args))

            self.engine.write(sql,args)
            self.parent.on_open()
                
            if self.index is not None:
                self.parent.lstTests.see(self.index)
                self.parent.lstTests.selection_set(self.index)
                    
            self.on_cancel()
           
    def on_cancel(self, evt=None):
        self.destroy()

    def set_samples(self):

        index = 0
        self.dict_samples={}
        l = []

        sql = "SELECT sample_id, description FROM samples ORDER BY description ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_samples[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbSamples['values']=l

    def set_units(self):

        index = 0
        self.dict_units={}
        l = []

        sql = "SELECT unit_id, unit FROM units ORDER BY unit ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_units[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbUnits['values']=l         

    def get_values(self,):

        return [self.dict_samples[self.cbSamples.current()],
                self.dict_units[self.cbUnits.current()],
                self.test.get(),
                self.cvw.get(),
                self.cvb.get(),
                self.enable.get()]
    
    def set_values(self,):

        key = next(key for key, value in self.dict_samples.items() if value == self.selected_test[1])
        self.cbSamples.current(key)

        key = next(key for key, value in self.dict_units.items() if value == self.selected_test[2])
        self.cbUnits.current(key)
        
        self.test.set(self.selected_test[3])
        self.cvw.set(self.selected_test[4])
        self.cvb.set(self.selected_test[5])
        self.enable.set(self.selected_test[6])

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type,
                 trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            if text :
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True        
