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
        super().__init__(name='batch')  

        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.index = index
        self.grid()
        
        self.day =  IntVar()
        self.month =  IntVar()
        self.year =  IntVar()

        self.batch = StringVar()
        self.target = DoubleVar()
        self.sd = DoubleVar()
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

        Label(w, text="Batch:").grid(row=0, sticky=W)
        self.txtBatch = Entry(w, bg='white', textvariable=self.batch)
        self.txtBatch.grid(row=0, column=1, padx=5, pady=5)
       
        Label(w, text="Expiration:").grid(row=1,column=0,sticky=W)

        self.engine.get_calendar(self,w,1)

        Label(w, text="Target:").grid(row=2, sticky=W)
        self.txtTarget = Entry(w,
                               bg='white',
                               validate = 'key',
                               validatecommand = self.vcmd,
                               textvariable=self.target)
        self.txtTarget.grid(row=2, column=1, padx=5, pady=5)
       
        Label(w, text="SD:").grid(row=3, sticky=W)
        self.txtSD = Entry(w,
                           bg='white',
                           validate = 'key',
                           validatecommand = self.vcmd,
                           textvariable=self.sd)
        self.txtSD.grid(row=3, column=1, padx=5, pady=5)
        
        Label(w, text="Enable:").grid(row=4, sticky=W)
        self.ckEnable = Checkbutton(w, onvalue=1, offvalue=0, variable = self.enable,)
        self.ckEnable.grid(row=4, column=1,sticky=W)

        self.engine.get_save_cancel(self, self) 
        

    def on_open(self, selected_test, selected_batch = None):

        self.selected_test = selected_test

        if selected_batch is not None:
            self.insert_mode = False
            self.selected_batch = selected_batch
            msg = "Update  %s" % (self.selected_batch[2],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new batch"
            self.enable.set(1)

        self.title(msg)
        self.txtBatch.focus()
        
    def on_save(self, evt=None):

        if self.engine.on_fields_control( (self.txtBatch,))==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.insert_mode == False:

                sql = self.engine.get_update_sql('batchs','batch_id')

                args = self.engine.get_update_sql_args(args, self.selected_batch[0])
                       
            elif self.insert_mode == True:

                sql = self.engine.get_insert_sql('batchs',len(args))

            self.engine.write(sql,args)
            
            if self.index is not None:
                self.parent.set_batches()
                self.parent.lstBatchs.see(self.index)
                self.parent.lstBatchs.selection_set(self.index)
                    
            self.on_cancel()

        else:
            messagebox.showinfo(self.engine.title,self.engine.abort)
               
            
    def on_cancel(self, evt=None):
        self.destroy()


    def get_values(self,):

        return (self.selected_test[0],
                self.batch.get(),
                self.engine.get_date(self,),
                self.target.get(),
                self.sd.get(),
                self.enable.get())
    
    def set_values(self,):

        self.year.set(int(self.selected_batch[3][0:4]))
        self.month.set(int(self.selected_batch[3][5:7]))
        self.day.set(int(self.selected_batch[3][8:10]))
        self.batch.set(self.selected_batch[2])
        self.target.set(self.selected_batch[4])
        self.sd.set(self.selected_batch[5])
        self.enable.set(self.selected_batch[6])
      

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
