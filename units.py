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
import unit

class Dialog(Toplevel):     
    def __init__(self,parent,engine):
        Toplevel.__init__(self,)

        self.resizable(0,0)
        self.parent = parent
        self.grid()
        self.engine = engine
    
        self.enable =  BooleanVar()
        
        self.panel = Frame(self, bd=5, padx = 5, pady = 5)
        
        self.tests = LabelFrame(self.panel,text='Units',)      

        self.scroll_bar = Scrollbar(self.tests,orient=VERTICAL)
        self.lstUnits = Listbox(self.tests,
                                relief=GROOVE,
                                selectmode=BROWSE,
                                bg='white',
                                yscrollcommand=self.scroll_bar.set,)
        self.lstUnits.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstUnits.bind("<Double-Button-1>", self.on_item_activated)
        self.scroll_bar.config(command=self.lstUnits.yview)

        self.lstUnits.pack(side=LEFT,fill=Y) 
        self.scroll_bar.pack(fill=Y, expand=1)
        self.tests.pack(fill=BOTH, side=LEFT,)


        self.buttons = Frame(self.panel, bd=5, padx = 5, pady = 5)
        
        self.btnAdd = Button(self.buttons, text="Add", command=self.on_add)
        self.btnAdd.pack(fill=X, padx=10, pady=5)

        self.btnEdit = Button(self.buttons, text="Edit", command=self.on_edit)
        self.btnEdit.pack(fill=X, padx=10, pady=5)

        self.btClose = Button(self.buttons, text="Close", command = self.on_cancel)
        self.btClose.pack(fill=X, padx=10, pady=5)

        self.buttons.pack(fill=BOTH, side=LEFT)

        self.panel.pack(fill=BOTH, expand=1)
 
      
    def on_open(self,):

        self.selected_unit = None

        sql = "SELECT * FROM units ORDER BY unit"

        rs = self.engine.read(True, sql, ())

        index = 0
        
        self.dict_units={}

        if rs:
            self.lstUnits.delete(0, END)
            for i in rs:
                self.lstUnits.insert(END, i[1])
                if i[2] != 1:
                    self.lstUnits.itemconfig(index, {'bg':'light gray'})
                self.dict_units[index]=i[0]
                index+=1
                
        self.title("Units")

    def on_add(self,):

        obj = unit.Dialog(self,self.engine)
        obj.attributes("-topmost", True)
        obj.on_open()
        obj.wait_visibility()
        obj.grab_set()
        self.wait_window(obj)

    def on_edit(self,):
        
        if self.selected_unit is not None:
            obj = unit.Dialog(self,self.engine,self.index)
            obj.attributes("-topmost", True)
            obj.on_open(self.selected_unit,)
            obj.wait_visibility()
            obj.grab_set()
            self.wait_window(obj)
        else:
            msg = "Please select an item."
            tkMessageBox.showwarning(self.engine.title,msg)

    def on_item_activated(self,event):

        self.on_edit()

    def on_item_selected(self,event):

        self.index = self.lstUnits.curselection()[0]
        pk = self.dict_units.get(self.index)
        self.selected_unit = self.engine.get_selected('units','unit_id', pk)

    def on_cancel(self,):
        self.destroy()
    
