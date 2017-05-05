#!/usr/bin/python
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------
from Tkinter import *
import tkMessageBox
import datetime

class Dialog(Toplevel):     
    def __init__(self,parent,selected_test,engine,index = None):
        Toplevel.__init__(self,)

        self.resizable(0,0)
        self.parent = parent
        self.grid()
        self.selected_test = selected_test
        self.engine = engine
        self.index = index

        self.day =  IntVar()
        self.month =  IntVar()
        self.year =  IntVar()

        self.batch = StringVar()
        self.target = DoubleVar()
        self.sd = DoubleVar()
        self.enable =  BooleanVar()

        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.panel = Frame(self, bd=5, padx = 5, pady = 5)
        self.panel.grid(row = 0, column = 0, sticky=N+W+S+E)

        Label(self.panel, text="Batch:").grid(row=0, sticky=W)
        self.txtBatch = Entry(self.panel, bg='white', textvariable=self.batch)
        self.txtBatch.grid(row=0, column=1, padx=5, pady=5)
       
        Label(self.panel, text="Exp Day:").grid(row=1, sticky=W)
        self.spDay = Spinbox(self.panel,bg='white',
                               from_=1,
                               to=31,
                               textvariable=self.day)
        self.spDay.config(repeatdelay=200)

        Label(self.panel, text="Exp Month:").grid(row=2, sticky=W)
        self.spMonth = Spinbox(self.panel,bg='white',
                               from_=1,
                               to=12,
                               textvariable=self.month)

        Label(self.panel, text="Exp Year:").grid(row=3, sticky=W)
        self.spYear = Spinbox(self.panel,bg='white',
                               from_=1900,
                               to=3000,
                               textvariable=self.year)

        self.spDay.grid(row=1,column=1,sticky=E, padx=5, pady=5)
        self.spMonth.grid(row=2,column=1,sticky=E, padx=5, pady=5)
        self.spYear.grid(row=3,column=1,sticky=E, padx=5, pady=5)

        Label(self.panel, text="Target:").grid(row=4, sticky=W)
        self.txtTarget = Entry(self.panel,
                               bg='white',
                               validate = 'key',
                               validatecommand = vcmd,
                               textvariable=self.target)
        self.txtTarget.grid(row=4, column=1, padx=5, pady=5)
       
        Label(self.panel, text="SD:").grid(row=5, sticky=W)
        self.txtSD = Entry(self.panel,
                           bg='white',
                           validate = 'key',
                           validatecommand = vcmd,
                           textvariable=self.sd)
        self.txtSD.grid(row=5, column=1, padx=5, pady=5)
        
        self.buttons = Frame(self, bd=5, padx = 5, pady = 5)
        self.buttons.grid(row = 0, column = 2, sticky=N+W+S+E)
       
        self.btnSave = Button(self.buttons,text="Save", command=self.on_save)
        self.btnSave.grid(row=0, column=2, sticky=W+E, padx=5, pady=5)
        
        self.btCancel = Button(self.buttons, text="Cancel", command=self.on_cancel)
        self.btCancel.grid(row=1, column=2, sticky=W+E, padx=5, pady=5)

        self.ckEnable = Checkbutton(self.buttons, text="Enable",onvalue=1, offvalue=0,variable = self.enable, )
        self.ckEnable.grid(row=2, column=2)
        

    def on_open(self,selected_batch = None):

        if selected_batch is not None:
            self.insert_mode = False
            self.selected_batch = selected_batch
            msg = "Update  %s" % (self.selected_batch[2],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new batch"
            self.enable.set(1)

        self.title(msg)
        self.txtBatch.focus()
        
    def on_save(self,):

        if self.on_fields_control()==False:

            msg = "Please fill all fields."
            tkMessageBox.showwarning(self.engine.title,msg)

        else:
       
            if tkMessageBox.askquestion(self.engine.title, "Do you want to save?"):

                args =  self.get_values()

                if self.insert_mode == False:

                    sql = self.engine.get_update_sql('batchs','batch_id')

                    args = self.engine.get_update_sql_args(args, self.selected_batch[0])
                       
                elif self.insert_mode == True:

                        sql = self.engine.get_insert_sql('batchs',len(args))

                self.engine.write(sql,args)
                self.parent.set_values(self.parent.lstBatchs)
                
                if self.index is not None:
                    self.parent.lstBatchs.see(self.index)
                    self.parent.lstBatchs.selection_set(self.index)
                    
                self.on_cancel()
            else:
                msg = "Operation aborted."
                tkMessageBox.showinfo(self.engine.title,msg)
           
    def on_cancel(self,):
        self.destroy()


    def get_values(self,):

        expiration = datetime.datetime(int(self.spYear.get()), int(self.spMonth.get()), int(self.spDay.get()))

        return (self.selected_test[0],
                self.batch.get(),
                expiration,
                self.target.get(),
                self.sd.get(),
                self.enable.get())
    
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

        objs = (self.txtBatch,)

        for obj in objs:
            if not obj.get():
                ret = False
                break   
            else:
                ret = True
        return ret                
                
        
