#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------

from Tkinter import *
import tkMessageBox
import ttk

class Dialog(Toplevel):     
    def __init__(self,parent,engine,index = None):
        Toplevel.__init__(self,)

        self.resizable(0,0)
        self.parent = parent
        self.grid() 
        self.engine = engine
        self.index = index

        self.test = StringVar()
        self.cvw = DoubleVar()
        self.cvb = DoubleVar()
        self.enable =  BooleanVar()
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.panel = Frame(self, bd=5, padx = 5, pady = 5)
        self.panel.grid(row = 0, column = 0, sticky=N+W+S+E)

        Label(self.panel, text="Samples:").grid(row=0, sticky=W)
        self.cbSamples =  ttk.Combobox(self.panel)
        self.cbSamples.grid(row=0, column=1, padx=5, pady=5)

        Label(self.panel, text="Units:").grid(row=1, sticky=W)
        self.cbUnits =  ttk.Combobox(self.panel,)
        self.cbUnits.grid(row=1, column=1, padx=5, pady=5)

        Label(self.panel, text="Test:").grid(row=2, sticky=W)
        self.txtTest = Entry(self.panel, bg='white', textvariable=self.test)
        self.txtTest.grid(row=2, column=1, padx=5, pady=5)

        Label(self.panel, text="Cvw:").grid(row=3, sticky=W)
        self.txtCVW = Entry(self.panel,
                            bg='white',
                            validate = 'key',
                            validatecommand = vcmd,
                            textvariable=self.cvw)
        self.txtCVW.grid(row=3, column=1, padx=5, pady=5)

        Label(self.panel, text="Cvb:").grid(row=4, sticky=W)
        self.txtCVB = Entry(self.panel,
                            bg='white',
                            validate = 'key',
                            validatecommand = vcmd,
                            textvariable=self.cvb)
        self.txtCVB.grid(row=4, column=1, padx=5, pady=5)

        self.buttons = Frame(self, bd=5, padx = 5, pady = 5)
        self.buttons.grid(row = 0, column = 2, sticky=N+W+S+E)
       
        self.btnSave = Button(self.buttons,text="Save", command=self.on_save)
        self.btnSave.grid(row=0, column=2, sticky=W+E, padx=5, pady=5)
        
        self.btCancel = Button(self.buttons, text="Cancel", command=self.on_cancel)
        self.btCancel.grid(row=1, column=2, sticky=W+E, padx=5, pady=5)

        self.ckEnable = Checkbutton(self.buttons, text="Enable",onvalue=1, offvalue=0,variable = self.enable, )
        self.ckEnable.grid(row=2, column=2)

    def on_open(self,selected_test = None):

        self.set_samples()
        self.set_units()
       
        if selected_test is not None:
            self.insert_mode = False
            self.selected_test = selected_test
            msg = "Update  %s" % (self.selected_test[3],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new test"
            self.enable.set(1)

        self.title(msg)
        self.txtTest.focus()
        
    def on_save(self,):

        if self.on_fields_control()==False:

            msg = "Please fill all fields."
            tkMessageBox.showwarning(self.engine.title,msg)

        else:
       
            if tkMessageBox.askquestion(self.engine.title, "Do you want to save?"):

                args =  self.get_values()

                if self.insert_mode == False:

                    sql = self.engine.get_update_sql('tests','test_id')

                    args = self.engine.get_update_sql_args(args, self.selected_test[0])
                       
                elif self.insert_mode == True:

                        sql = self.engine.get_insert_sql('tests',len(args))

                self.engine.write(sql,args)
                self.parent.on_open()
                
                if self.index is not None:
                    self.parent.lstTests.see(self.index)
                    self.parent.lstTests.selection_set(self.index)
                    
                self.on_cancel()
           
    def on_cancel(self,):
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

        return (self.dict_samples[self.cbSamples.current()],
                self.dict_units[self.cbUnits.current()],
                self.test.get(),
                self.cvw.get(),
                self.cvb.get(),
                self.enable.get())
    
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
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True        

    def on_fields_control(self):

        objs = (self.txtTest,)

        for obj in objs:
            if not obj.get():
                ret = False
                break   
            else:
                ret = True
        return ret                
                
        
