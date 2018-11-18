#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter
# version:  0.1                                                                
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox
import frames.test

class Dialog(Toplevel):     
    def __init__(self,parent, engine):
        super().__init__(name='tests')

        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = engine
        
        self.enable =  BooleanVar()
        self.selected_item = None
        self.obj = None

        self.center_me()
        self.init_ui()

    def center_me(self):
        #center window
        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))
        

    def init_ui(self):
    
        p = self.engine.get_frame(self)

        w = Frame(p,)
        self.lstItems = self.engine.get_listbox(w,)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        w.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)

        self.engine.get_add_edit_cancel(self,p)

        p.pack(side=LEFT, fill=BOTH, expand=1)

        
    def on_open(self,):

        sql = "SELECT tests.test_id,tests.test||' '||samples.sample, tests.enable\
               FROM tests\
               INNER JOIN samples ON tests.sample_id = samples.sample_id\
               ORDER BY tests.test"

        rs = self.engine.read(True, sql, ())

        index = 0

        self.dict_items={}

        if rs:
            self.lstItems.delete(0, END)
            for i in rs:
                s = "{:}".format(i[1])
                self.lstItems.insert(END, s)
                if i[2] != 1:
                    self.lstItems.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index]=i[0]
                index+=1
                        
        self.title("Tests")

    def on_add(self, evt):

        self.obj = frames.test.Dialog(self,self.engine)
        self.obj.transient(self)
        self.obj.on_open()

    def on_edit(self, evt):
        self.on_item_activated()
        

    def on_item_activated(self, evt=None):

        if self.lstItems.curselection():
            if self.selected_item is not None:
                self.obj = frames.test.Dialog(self,self.engine,self.index)
                self.obj.transient(self)
                self.obj.on_open(self.selected_item,)
               
            else:
                messagebox.showwarning(self.engine.title,self.engine.no_selected)
                
    def on_item_selected(self, evt):

        if self.lstItems.curselection():
            try:
                self.index = self.lstItems.curselection()[0]
                pk = self.dict_items.get(self.index)
                self.selected_item = self.engine.get_selected('tests','test_id', pk)
            except:
                self.dict_items = None
                self.index = 0  

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
    
