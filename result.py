#!/usr/bin/python3
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
    def __init__(self,parent,selected_batch,engine,index = None):
        Toplevel.__init__(self,)

        self.resizable(0,0)
        self.parent = parent
        self.grid()
        self.selected_batch = selected_batch
        self.engine = engine
        self.index = index

        self.day =  IntVar()
        self.month =  IntVar()
        self.year =  IntVar()

        self.result = DoubleVar()
        self.enable =  BooleanVar()

        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.panel = Frame(self, bd=5, padx = 5, pady = 5)
        self.panel.grid(row = 0, column = 0, sticky=N+W+S+E)
        
        Label(self.panel, text="Result:").grid(row=0, sticky=W)

        self.txtResult = Entry(self.panel, bg='white',validate = 'key', validatecommand = vcmd, textvariable=self.result)
        self.txtResult.grid(row=0, column=1)
        
        Label(self.panel, text="Recived Day:").grid(row=1, sticky=W)
        self.spDay = Spinbox(self.panel,bg='white',
                               from_=1,
                               to=31,
                               textvariable=self.day)
        self.spDay.config(repeatdelay=200)

        Label(self.panel, text="Recived Month:").grid(row=2, sticky=W)
        self.spMonth = Spinbox(self.panel,bg='white',
                               from_=1,
                               to=12,
                               textvariable=self.month)

        Label(self.panel, text="Recived Year:").grid(row=3, sticky=W)
        self.spYear = Spinbox(self.panel,bg='white',
                               from_=1900,
                               to=3000,
                               textvariable=self.year)

        self.spDay.grid(row=1,column=1,sticky=E, padx=5, pady=5)
        self.spMonth.grid(row=2,column=1,sticky=E, padx=5, pady=5)
        self.spYear.grid(row=3,column=1,sticky=E, padx=5, pady=5)

        
        self.buttons = Frame(self, bd=5, padx = 5, pady = 5)
        self.buttons.grid(row = 0, column = 2, sticky=N+W+S+E)
       
        self.btnSave = Button(self.buttons,text="Save", command=self.on_save)
        self.btnSave.grid(row=0, column=2, sticky=W+E, padx=5, pady=5)
        
        self.btCancel = Button(self.buttons, text="Cancel", command=self.on_cancel)
        self.btCancel.grid(row=1, column=2, sticky=W+E, padx=5, pady=5)

        self.ckEnable = Checkbutton(self.buttons, text="Enable",onvalue=1, offvalue=0,variable = self.enable, )
        self.ckEnable.grid(row=2, column=2)
        

    def on_open(self,selected_result = None):

        if selected_result is not None:
            self.insert_mode = False
            self.selected_result = selected_result
            msg = "Update  %s" % (self.selected_result[2],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new result"
            self.enable.set(1)

        self.title(msg)
        self.txtResult.focus()
        
    def on_save(self,):

        if self.on_fields_control()==False:

            msg = "Please fill all fields."
            tkMessageBox.showwarning(self.engine.title,msg)

        else:
       
            if tkMessageBox.askquestion(self.engine.title, "Do you want to save?"):

                args =  self.get_values()

                if self.insert_mode == False:

                    sql = self.engine.get_update_sql('results','result_id')

                    args = self.engine.get_update_sql_args(args, self.selected_result[0])
                       
                elif self.insert_mode == True:

                        sql = self.engine.get_insert_sql('results',len(args))

                self.engine.write(sql,args)
                self.parent.set_values(self.parent.lstResults)
                
                if self.index is not None:
                    self.parent.lstResults.see(self.index)
                    self.parent.lstResults.selection_set(self.index)
                    
                self.on_cancel()
            else:
                msg = "Operation aborted."
                tkMessageBox.showinfo(self.engine.title,msg)
           
    def on_cancel(self,):
        self.destroy()


    def get_values(self,):

        recived = datetime.datetime(int(self.spYear.get()), int(self.spMonth.get()), int(self.spDay.get()))

        return (self.selected_batch[0],
                self.result.get(),
                recived,
                self.enable.get())
    
    def set_values(self,):

        self.year.set(int(self.selected_result[3][0:4]))
        self.month.set(int(self.selected_result[3][5:7]))
        self.day.set(int(self.selected_result[3][8:10]))

        self.result.set(self.selected_result[2])
        self.enable.set(self.selected_result[4])

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

        objs = (self.txtResult,)

        for obj in objs:
            if not obj.get():
                ret = False
                break   
            else:
                ret = True
        return ret                
                
