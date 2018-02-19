#-----------------------------------------------------------------------------
# project:  biovrase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018
# version:  0.1                                                                
#-----------------------------------------------------------------------------
from tkinter import *
from tkinter import messagebox

class Dialog(Toplevel):     
    def __init__(self,parent,engine, index = None):
        super().__init__(name='unit')
        
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.index = index
        self.grid()

        self.unit = StringVar()
        self.enable =  BooleanVar()
        
        self.center_me()
        self.init_ui()

    def center_me(self):
        
        """center window on the screen"""
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2
        self.geometry("+%d+%d" % (x, y))

    def cols_configure(self,w):
        
        w.columnconfigure(0, weight=1)
        w.columnconfigure(1, weight=1)
        w.columnconfigure(2, weight=1)        


    def init_ui(self):

        w = Frame(self, bd=1, padx = 5, pady = 5)
        self.cols_configure(w)
        w.grid(row = 0, column = 0, sticky=N+W+S+E)

        Label(w, text="Unit:").grid(row=0, sticky=W)
        self.txtUnit = Entry(w, bg='white', textvariable=self.unit)
        self.txtUnit.grid(row=0, column=1, padx=5, pady=5)

        Label(w, text="Enable:").grid(row=1, sticky=W)
        self.ckEnable = Checkbutton(w, onvalue=1, offvalue=0, variable = self.enable,)
        self.ckEnable.grid(row=1, column=1,sticky=W)
        
        self.engine.get_save_cancel(self, self) 

    def on_open(self,selected_item = None):

        if selected_item is not None:
            self.insert_mode = False
            self.selected_item = selected_item
            msg = "Update  unit %s" % (self.selected_item[1],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new unit"
            self.enable.set(1)

        self.title(msg)
        self.txtUnit.focus()

    def set_values(self,):
        
        self.unit.set(self.selected_item[1])
        self.enable.set(self.selected_item[2])        

    def get_values(self,):

        return (self.unit.get(),
                self.enable.get(),)

    def on_save(self, evt):

        if self.on_fields_control()==False:return

        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.insert_mode == False:

                sql = self.engine.get_update_sql('units','unit_id')

                args = self.engine.get_update_sql_args(args, self.selected_item[0])
                   
            elif self.insert_mode == True:

                    sql = self.engine.get_insert_sql('units',len(args))

            self.engine.write(sql,args)
            self.parent.on_open()
            
            if self.index is not None:
                
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)
                
            self.on_cancel()

        else:
            messagebox.showinfo(self.engine.title, self.engine.abort)
           
    def on_cancel(self, evt=None):
        self.destroy()

    def on_fields_control(self):
        fields = (self.txtUnit,)
        return self.engine.on_fields_control(fields)                
