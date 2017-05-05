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
import ttk

class Dialog(Toplevel):     
    def __init__(self,parent,engine,index = None):
        Toplevel.__init__(self,)

        self.resizable(0,0)
        self.parent = parent
        self.grid() 
        self.engine = engine
        self.index = index

        self.unit = StringVar()
        self.enable =  BooleanVar()

        self.panel = Frame(self, bd=5, padx = 5, pady = 5)
        self.panel.grid(row = 0, column = 0, sticky=N+W+S+E)

        Label(self.panel, text="unit:").grid(row=0, sticky=W)
        self.txtUnit = Entry(self.panel, bg='white', textvariable=self.unit)
        self.txtUnit.grid(row=0, column=1, padx=5, pady=5)

        self.buttons = Frame(self, bd=5, padx = 5, pady = 5)
        self.buttons.grid(row = 0, column = 2, sticky=N+W+S+E)
       
        self.btnSave = Button(self.buttons,text="Save", command=self.on_save)
        self.btnSave.grid(row=0, column=2, sticky=W+E, padx=5, pady=5)
        
        self.btCancel = Button(self.buttons, text="Cancel", command=self.on_cancel)
        self.btCancel.grid(row=1, column=2, sticky=W+E, padx=5, pady=5)

        self.ckEnable = Checkbutton(self.buttons, text="Enable",onvalue=1, offvalue=0,variable = self.enable, )
        self.ckEnable.grid(row=2, column=2)

        
    def on_open(self,selected_unit = None):

        if selected_unit is not None:
            self.insert_mode = False
            self.selected_unit = selected_unit
            msg = "Update  %s" % (self.selected_unit[1],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new unit"
            self.enable.set(1)

        self.title(msg)
        self.txtUnit.focus()
        
    def on_save(self,):

        if self.on_fields_control()==False:

            msg = "Please fill all fields."
            tkMessageBox.showwarning(self.engine.title,msg)

        else:
       
            if tkMessageBox.askquestion(self.engine.title, "Do you want to save?"):

                args =  self.get_values()

                if self.insert_mode == False:

                    sql = self.engine.get_update_sql('units','unit_id')

                    args = self.engine.get_update_sql_args(args, self.selected_unit[0])
                       
                elif self.insert_mode == True:

                        sql = self.engine.get_insert_sql('units',len(args))

                self.engine.write(sql,args)
                self.parent.on_open()
                
                if self.index is not None:
                    self.parent.lstUnits.see(self.index)
                    self.parent.lstUnits.selection_set(self.index)
                    
                self.on_cancel()
           
    def on_cancel(self,):
        self.destroy()

      
    def get_values(self,):

        return (self.unit.get(),
                self.enable.get())
    
    def set_values(self,):

        self.unit.set(self.selected_unit[1])
        self.enable.set(self.selected_unit[2])

    def on_fields_control(self):

        objs = (self.txtUnit,)

        for obj in objs:
            if not obj.get():
                ret = False
                break   
            else:
                ret = True
        return ret                
                
        
