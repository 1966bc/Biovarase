#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox
import datetime

import frames.rejection

class Dialog(Toplevel):     
    def __init__(self,parent, engine):
        super().__init__(name='rejections')

        #self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = engine
        self.test = StringVar()
        self.batch = StringVar()
        self.result = StringVar()
        self.recived = StringVar()
        self.enable =  BooleanVar()
        self.selected_item = None
        self.obj = None

        self.cols = (["#0",'id','w',False,0,0],
                      ["#1",'Date','w',True,80,80],
                      ["#2",'Action','w',True,100,100],
                      ["#3",'Description','w',True,200,200],)

        self.center_me()
        self.init_ui()

    def center_me(self):
        #center window
        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))
        
    def init_ui(self):
    
        p = self.engine.get_frame(self)

        w = LabelFrame(p,text='Select data',)

        Label(w, text="Test:").pack(side=TOP)
        Label(w,
              font = "Verdana 12 bold",
              textvariable = self.test).pack(side=TOP)

        Label(w, text="Batch:").pack(side=TOP)
        Label(w,
              font = "Verdana 12 bold",
              textvariable = self.batch).pack(side=TOP)

        Label(w, text="Result:").pack(side=TOP)
        Label(w,
              font = "Verdana 12 bold",
              textvariable = self.result).pack(side=TOP)

        Label(w, text="Recived:").pack(side=TOP)
        Label(w,
              font = "Verdana 12 bold",
              textvariable = self.recived).pack(side=TOP)

        w.pack(side=LEFT, fill=Y, expand=0)

        w = Frame(p,)
        
        self.lstItems = self.engine.get_tree(w, self.cols,)
        self.lstItems.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-1>", self.on_item_activated)
              
        w.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)

        self.engine.get_add_edit_cancel(self,p)

        p.pack(side=LEFT, fill=BOTH, expand=1)

    def on_open(self, selected_test, selected_batch, selected_result):

        self.selected_test = selected_test 
        self.selected_batch = selected_batch 
        self.selected_result = selected_result

        self.test.set(selected_test[1])
        self.batch.set(selected_batch[2])
        self.result.set(selected_result[2])

        dt = selected_result[3].strftime('%Y-%m-%d')
        
        self.recived.set(dt)

        sql = "SELECT * FROM lst_rejections WHERE result_id =?"
        args = (selected_result[0],)
        rs = self.engine.read(True, sql, args)

        for i in self.lstItems.get_children():
            self.lstItems.delete(i)

        if rs:
            for i in rs:
                self.lstItems.insert('', 0, text=i[0],values=(i[3],i[1],i[2]))
                

        self.title("Rejections")

    def on_add(self, evt):

        self.obj = frames.rejection.Dialog(self,self.engine)
        self.obj.on_open(self.selected_test,self.selected_batch, self.selected_result)

    def on_edit(self, evt):
        self.on_item_activated()
        

    def on_item_activated(self, evt=None):

        if self.selected_item is not None:
            obj = frames.rejection.Dialog(self,self.engine)
            obj.transient(self)
            obj.on_open(self.selected_test,self.selected_batch, self.selected_result, self.selected_item)
        else:
            messagebox.showwarning(self.engine.title,self.engine.no_selected)

                
    def on_item_selected(self, evt):

        pk = int(self.lstItems.item(self.lstItems.focus())['text'])
        self.selected_item = self.engine.get_selected('rejections','rejection_id', pk)

            
    def on_cancel(self, evt=None):

        """force closing of the childs...
        """     
        
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
    
