#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018                                                          
#-----------------------------------------------------------------------------
from tkinter import *
from tkinter import messagebox

class Dialog(Toplevel):     
    def __init__(self,parent, engine, index = None):
        super().__init__(name='result')  

        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.index = index
        self.grid()
        
        self.day =  IntVar()
        self.month =  IntVar()
        self.year =  IntVar()

        self.result = DoubleVar()
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

        Label(w, text="Result:").grid(row=0, sticky=W)
        self.txtResult = Entry(w,
                               bg='white',
                               validate = 'key',
                               validatecommand = self.vcmd,
                               textvariable=self.result)
        self.txtResult.grid(row=0, column=1, padx=5, pady=5)

        Label(w, text="Recived:").grid(row=1,column=0,sticky=W)

        self.engine.get_calendar(self,w,1)

        Label(w, text="Enable:").grid(row=4, sticky=W)
        self.ckEnable = Checkbutton(w, onvalue=1, offvalue=0, variable = self.enable,)
        self.ckEnable.grid(row=4, column=1,sticky=W)

        self.engine.get_save_cancel(self, self) 


    def on_open(self, selected_batch, selected_result = None):

        self.selected_batch = selected_batch

        if selected_result is not None:
            self.insert_mode = False
            self.selected_result = selected_result
            msg = "Update  %s" % (self.selected_result[2],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new result"
            self.enable.set(1)

        self.title(msg)
        self.txtResult.focus()
        
    def on_save(self, evt=None):

        if self.engine.on_fields_control( (self.txtResult,))==False:return
        if self.engine.get_date(self) is not False:
            if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

                args =  self.get_values()

                if self.insert_mode == False:

                    sql = self.engine.get_update_sql('results','result_id')

                    args = self.engine.get_update_sql_args(args, self.selected_result[0])
        
                elif self.insert_mode == True:

                    sql = self.engine.get_insert_sql('results',len(args))


                self.engine.write(sql,args)
                self.parent.set_values(self.parent.lstResults)
                    
                if self.index is not None:
                    self.parent.lstResults.see(self.index)
                    self.parent.lstResults.selection_set(self.index)
                        
                self.on_cancel()

            else:
                messagebox.showinfo(self.engine.title,self.engine.abort)
           
    def on_cancel(self, evt=None):
        self.destroy()


    def get_values(self,):

        return (self.selected_batch[0],
                self.result.get(),
                self.engine.get_timestamp(self),
                self.enable.get())
    
    def set_values(self,):
        
        self.year.set(int(self.selected_result[3].year))
        self.month.set(int(self.selected_result[3].month))
        self.day.set(int(self.selected_result[3].day))

        self.result.set(self.selected_result[2])
        self.enable.set(self.selected_result[4])

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type,
                 trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            if text:
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True    
         
