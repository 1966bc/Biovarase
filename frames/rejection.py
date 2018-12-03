#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn 2018                                                        
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox

class Dialog(Toplevel):     
    def __init__(self,parent, engine, index = None):
        super().__init__(name='rejection')
        
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        #self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.index = index
        self.grid()

        self.day =  IntVar()
        self.month =  IntVar()
        self.year =  IntVar()

        self.description = StringVar()
        self.enable =  BooleanVar()
        self.vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

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

        w = self.engine.get_frame(self)        
        self.cols_configure(w)
        w.grid(row = 0, column = 0, sticky=N+W+S+E)

        Label(w, text="Actions:").grid(row=0, sticky=W)
        self.cbActions = ttk.Combobox(w,)
        self.cbActions.grid(row=0, column=1)

        Label(w, text="Description:").grid(row=1, sticky=W)
        self.txDescription = Entry(w, bg='white', textvariable=self.description,)
        self.txDescription.grid(row=1, column=1, padx=5, pady=5,ipady=2)

        Label(w, text="Modified:").grid(row=2,column=0,sticky=W)
        self.engine.get_calendar(self,w,2)

        Label(w, text="Enable:").grid(row=3, sticky=W)
        Checkbutton(w, onvalue=1, offvalue=0, variable = self.enable,).grid(row=3, column=1,sticky=W)

        self.engine.get_save_cancel(self, self)

    def on_open(self, selected_test, selected_batch, selected_result, selected_rejection = None):

        self.selected_test = selected_test
        self.selected_batch = selected_batch
        self.selected_result = selected_result

        self.set_actions()
          
        if selected_rejection is not None:
            self.insert_mode = False
            self.selected_rejection = selected_rejection
            msg = "Update rejection"
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Add rejection"
            self.enable.set(1)
            self.engine.set_date(self)

        self.title(msg)
        self.cbActions.focus()
        
    def on_save(self, evt=None):

        if self.engine.on_fields_control( (self.txDescription,))==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.insert_mode == False:

                sql = self.engine.get_update_sql('rejections','rejection_id')

                args = self.engine.get_update_sql_args(args, self.selected_rejection[0])
                       
            elif self.insert_mode == True:

                    sql = self.engine.get_insert_sql('rejections',len(args))

            self.engine.write(sql,args)
            self.parent.on_open(self.selected_test,self.selected_batch,self.selected_result)        
            self.on_cancel()
           
    def on_cancel(self, evt=None):
        self.destroy()

    def set_actions(self):

        index = 0
        self.dict_actions={}
        l = []

        sql = "SELECT action_id, action FROM actions ORDER BY action ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_actions[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbActions['values']=l
 

    def get_values(self,):

        return (self.selected_result[0],
                self.dict_actions[self.cbActions.current()],
                self.description.get(),
                self.engine.get_timestamp(self),
                self.enable.get())
    
    def set_values(self,):

        key = next(key for key, value in self.dict_actions.items() if value == self.selected_rejection[2])
        self.cbActions.current(key)

        self.description.set(self.selected_rejection[3])

        self.year.set(int(self.selected_rejection[4].year))
        self.month.set(int(self.selected_rejection[4].month))
        self.day.set(int(self.selected_rejection[4].day))
      
        self.enable.set(self.selected_rejection[5])

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type,
                 trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            if text :
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True        
