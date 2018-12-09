#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox
import frames.action as action

class Dialog(Toplevel):     
    def __init__(self,parent, engine):
        super().__init__(name='actions')

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
    
        f0 = self.engine.get_frame(self)

        f1 = Frame(f0,)
        self.lstActions = self.engine.get_listbox(f1,)
        self.lstActions.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstActions.bind("<Double-Button-1>", self.on_item_activated)
        f1.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)

        self.engine.get_add_edit_cancel(self,f0)

        f0.pack(side=LEFT, fill=BOTH, expand=1)

        
    def on_open(self,):

        sql = "SELECT * FROM actions"

        rs = self.engine.read(True, sql, ())

        index = 0

        self.dict_items={}

        if rs:
            self.lstActions.delete(0, END)
            for i in rs:
                self.lstActions.insert(END, i[1])
                if i[2] != 1:
                    self.lstActions.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index]=i[0]
                index+=1
                        
        self.title("Correttive Actions")

    def on_add(self, evt):

        self.obj = action.Dialog(self,self.engine)
        self.obj.on_open()

    def on_edit(self, evt):
        self.on_item_activated()
        
    def on_item_activated(self, evt=None):

        if self.lstActions.curselection():
            index = self.lstActions.curselection()[0]
            self.obj = action.Dialog(self,self.engine,index)
            self.obj.transient(self)
            self.obj.on_open(self.selected_item,)
               
        else:
            messagebox.showwarning(self.engine.title,self.engine.no_selected)
                
    def on_item_selected(self, evt):

        if self.lstActions.curselection():
            index = self.lstActions.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.engine.get_selected('actions','action_id', pk)
            
    def on_cancel(self, evt=None):

        """force closing of the childs...
        """     
        
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
    
