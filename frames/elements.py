#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   winter 2018
# version:  0.1                                                                
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox

class Dialog(Toplevel):     
    def __init__(self,parent,engine, index = None):
        super().__init__(name='elements')

        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.grid()
       
        self.elements = IntVar()

        self.center_me()
        self.init_ui()

    def center_me(self):
        #center window
        x = (self.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() - self.master.winfo_reqheight()) / 2
        self.geometry("+%d+%d" % (x, y))

    def cols_configure(self,w):
        
        w.columnconfigure(0, weight=1)
        w.columnconfigure(1, weight=1)
        w.columnconfigure(2, weight=1)
        
    def init_ui(self):  

        w = Frame(self, bd=5, padx = 5, pady = 5)
        self.cols_configure(w)
        w.grid(row = 0, column = 0, sticky=N+W+S+E)
        
        Label(w, text="Elements:").grid(row=0, sticky=W)
        self.txtElements = Entry(w, bg='white', textvariable=self.elements)
        self.txtElements['validatecommand'] = (self.txtElements.register(self.validate_integer),'%P','%i','%d')
        self.txtElements.grid(row=0, column=1, padx=5, pady=5)
        
        self.engine.get_save_cancel(self, self)
       
    def on_open(self,):
        
        self.title('Set elements')
        self.set_values()

    def set_values(self,):
        self.elements.set(self.engine.get_elements())
        self.txtElements.focus()        
        
    def on_save(self, evt=None):

        if self.engine.on_fields_control( (self.txtElements,))==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:
            try:
                sql = "UPDATE elements SET element =?"
                args = (self.elements.get(),)
                self.engine.write(sql, args)
                
                self.parent.set_elements()
                self.on_cancel()
            except:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])

    def on_cancel(self, evt=None):
        self.destroy()
   
    def validate_integer(self,x,i,acttyp):
        
        ind=int(i)
        if acttyp == '1': #insert
            if not x[ind].isdigit():
                return False
        return True        
