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
import test

class Dialog(Toplevel):     
    def __init__(self,parent,engine):
        Toplevel.__init__(self,)

        self.resizable(0,0)
        self.parent = parent
        self.grid()
        self.engine = engine
        self.enable =  BooleanVar()
        self.selected_test = None

        self.panel = Frame(self, bd=5, padx=5, pady=5)
        
        self.tests = LabelFrame(self.panel,text='Tests',)      

        self.scroll_bar = Scrollbar(self.tests,orient=VERTICAL)
        self.lstTests = Listbox(self.tests,
                                relief=GROOVE,
                                selectmode=BROWSE,
                                bg='white',
                                yscrollcommand=self.scroll_bar.set,)
        self.lstTests.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstTests.bind("<Double-Button-1>", self.on_item_activated)
        self.scroll_bar.config(command=self.lstTests.yview)

        self.lstTests.pack(side=LEFT,fill=Y) 
        self.scroll_bar.pack(fill=Y, expand=1)
        self.tests.pack(fill=BOTH, side=LEFT,)

        self.panel.pack(fill=BOTH, expand=1)

        self.buttons = Frame(self.panel, bd=5, padx=5, pady=5)
        
        self.btnAdd = Button(self.buttons, text="Add", command=self.on_add)
        self.btnAdd.pack(fill=X, padx=10, pady=5)

        self.btnEdit = Button(self.buttons, text="Edit", command=self.on_edit)
        self.btnEdit.pack(fill=X, padx=10, pady=5)

        self.btClose = Button(self.buttons, text="Close", command = self.on_cancel)
        self.btClose.pack(fill=X, padx=10, pady=5)

        self.buttons.pack(fill=BOTH, side=LEFT)

        
    def on_open(self,):

        sql = "SELECT tests.test_id,tests.test||' '||samples.sample, tests.enable\
               FROM tests\
               INNER JOIN samples ON tests.sample_id = samples.sample_id\
               ORDER BY tests.test"

        rs = self.engine.read(True, sql, ())

        index = 0
        self.dict_tests={}

        if rs:
            self.lstTests.delete(0, END)
            for i in rs:
                self.lstTests.insert(END, i[1])
                if i[2] != 1:
                    self.lstTests.itemconfig(index, {'bg':'light gray'})
                self.dict_tests[index]=i[0]
                index+=1
                
        self.title("Tests")

    def on_add(self,):

        obj = test.Dialog(self,self.engine)
        obj.attributes("-topmost", True)
        obj.on_open()
        obj.wait_visibility()
        obj.grab_set()
        self.wait_window(obj)

    def on_edit(self,):
        
        if self.selected_test is not None:
            obj = test.Dialog(self,self.engine,self.index)
            obj.attributes("-topmost", True)
            obj.on_open(self.selected_test,)
            obj.wait_visibility()
            obj.grab_set()
            self.wait_window(obj)
        else:
            msg = "Please select an item."
            tkMessageBox.showwarning(self.engine.title,msg)

    def on_item_activated(self,event):

        self.on_edit()

    def on_item_selected(self,event):

        self.index = self.lstTests.curselection()[0]
        pk = self.dict_tests.get(self.index)
        self.selected_test = self.engine.get_selected('tests','test_id', pk)

    def on_cancel(self,):
        self.destroy()
    
