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
import shelve

class Dialog(Toplevel):     
    def __init__(self,parent,engine):
        Toplevel.__init__(self,)

        #self.resizable(0,0)
        
        self.parent = parent
        self.grid()
        self.engine = engine
        self.elements = IntVar()

        self.panel = Frame(self, bd=5, padx = 5, pady = 5)
        self.panel.grid(row = 0, column = 0, sticky=N+W+S+E)
        
        Label(self.panel, text="Elements:").grid(row=0, sticky=W+E)
        self.txtElements = Entry(self.panel,relief="groove", bg='white', validate="key", textvariable=self.elements)
        self.txtElements['validatecommand'] = (self.txtElements.register(self.validate_integer),'%P','%i','%d')
        self.txtElements.grid(row=0, column=1, sticky=W+E)

        self.buttons = Frame(self, bd=5, padx = 5, pady = 5)
        self.buttons.grid(row = 0, column = 2, sticky=N+W+S+E)
        
        self.btnSave = Button(self.buttons,text="Save", command=self.on_save)
        self.btnSave.grid(row=0, column=2, sticky=W+E, padx=5, pady=5)
        
        self.btCancel = Button(self.buttons, text="Cancel", command=self.on_cancel)
        self.btCancel.grid(row=1, column=2, sticky=W+E, padx=5, pady=5)
       
    def on_open(self,):
        
        self.title('Set elements')

        self.engine.parameters = self.engine.get_parameters()
        
        self.set_values()
        
    def on_save(self,):

        if self.engine.on_fields_control( (self.txtElements,))==False:

            msg = "Please fill all fields."
            tkMessageBox.showwarning(self.engine.title,msg)

        else:            

            if tkMessageBox.askquestion(self.engine.title, "Do you want to save?"):

                try:
                    db = shelve.open('parameters')
                    db['elements'] = self.elements.get()
                    db.close()
                    self.parent.set_elements()
                    self.on_cancel()
                except:
                    print (sys.exc_info()[0])
                    print (sys.exc_info()[1])
                    print (sys.exc_info()[2])

    def on_cancel(self,):
        self.destroy()
    
    def set_values(self,):
        self.elements.set(self.engine.parameters['elements'])
        self.txtElements.focus()

    def validate_integer(self,x,i,acttyp):
        
        ind=int(i)
        if acttyp == '1': #insert
            if not x[ind].isdigit():
                return False
        return True        
