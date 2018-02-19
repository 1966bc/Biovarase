#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018
# version:  0.1                                                                
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox

import frames.batch as batch
import frames.result as result

class Dialog(Toplevel):     
    def __init__(self,parent, engine):
        super().__init__(name='data_manager')

        #self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = engine
        
        self.enable =  BooleanVar()
        self.obj = None

        self.selected_test = None
        self.selected_batch = None
        self.selected_result = None

        self.center_me()
        self.init_ui()

    def center_me(self):
        #center window
        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))
        

    def init_ui(self):
    
        p = self.engine.get_frame(self)
        
        w_tests = Frame(p,)
        w = LabelFrame(w_tests,text=  "Tests", padx = 5, pady = 5)
        self.lstTests = self.engine.get_listbox(w,)
        self.lstTests.bind("<<ListboxSelect>>", self.on_test_selected)
        w.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)
        w_tests.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)

        w_batchs = Frame(p,)
        msg = '{:<20}{:<12}{:<15}{:<20}'.format('Batchs','Expirations','Target','SD')
        w = LabelFrame(w_batchs,text= msg, padx = 5, pady = 5)
        self.lstBatchs = self.engine.get_listbox(w,)
        self.lstBatchs.bind("<<ListboxSelect>>", self.on_batch_selected)
        self.lstBatchs.bind("<Double-Button-1>", self.on_batch_activated)
        w.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)
        w_batchs.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)

        
        w_results = Frame(p,)
        s = '{:<15}{:<20}'.format('Recived','Result')
        w = LabelFrame(w_results,text=s, padx = 5, pady = 5)
        self.lstResults = self.engine.get_listbox(w,)
        self.lstResults.bind("<<ListboxSelect>>", self.on_result_selected)
        self.lstResults.bind("<Double-Button-1>", self.on_result_activated)
        w.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)
        w_results.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)
        
        bts = self.engine.get_frame(self)
        self.btnBatch = self.engine.get_button(bts, "Batch")
        self.btnBatch.bind("<Button-1>", self.on_add_batch)
        self.btnResult = self.engine.get_button(bts, "Result")
        self.btnResult.bind("<Button-1>", self.on_add_result)
        self.btClose = self.engine.get_button(bts, "Close")
        self.btClose.bind("<Button-1>", self.on_cancel)
        bts.pack(fill=BOTH, side=RIGHT)
        
        p.pack(fill=BOTH, expand=1, padx=5, pady=5)

        
    def on_open(self,):

        self.set_values(self.lstTests)
     
        self.title("Batchs and results management")

    def set_values(self, obj):

        index = 0

        if obj == self.lstTests:

            sql = "SELECT tests.test_id,tests.test||' '||samples.sample\
                   FROM tests\
                   INNER JOIN samples ON tests.sample_id = samples.sample_id\
                   ORDER BY tests.test"

            rs = self.engine.read(True, sql, ())

            self.dict_tests={}

            if rs:
                self.lstTests.delete(0, END)
                for i in rs:
                    self.lstTests.insert(END, i[1])
                    self.dict_tests[index]=i[0]
                    index+=1

        elif obj == self.lstBatchs:

            self.lstBatchs.delete(0, END)
            self.lstResults.delete(0, END)

            self.dict_batchs={}
            sql = "SELECT batch_id, batch,strftime('%d-%m-%Y', expiration), target, sd, enable FROM batchs WHERE test_id = ?"
            rs = self.engine.read(True, sql, (self.selected_test[0],))
            
            if rs:
                for i in rs:
                    s = '{:<20}{:<12}{:<10}{:<10}'.format(i[1],i[2],i[3],i[4])
                    #s = "%s %s %s %s"%(i[1],i[2],i[3],i[4])
                    self.lstBatchs.insert(END, (s))
                    if i[5] !=1:
                        self.lstBatchs.itemconfig(index, {'bg':'gray'})
                    self.dict_batchs[index]=i[0]
                    index+=1

        elif obj == self.lstResults:

            self.lstResults.delete(0, END)

            self.dict_results={}
            sql = "SELECT result_id, ROUND(result,2), strftime('%d-%m-%Y', recived),enable\
                   FROM results WHERE batch_id = ? ORDER BY recived DESC"
            rs = self.engine.read(True, sql, (self.selected_batch[0],))
            
            if rs:
                for i in rs:
                    s = '{:<15}{:<20}'.format(i[2],i[1])
                    self.lstResults.insert(END, (s))
                    if i[3] != 1:
                        self.lstResults.itemconfig(index, {'bg':'gray'})
                    self.dict_results[index]=i[0]
                    index+=1
            
    def on_test_selected(self,event):

        if self.lstTests.curselection():
            self.index = self.lstTests.curselection()[0]
            pk = self.dict_tests.get(self.index)
            self.selected_test = self.engine.get_selected('tests','test_id', pk)
            self.set_values(self.lstBatchs)
       
        
    def on_batch_selected(self, event):

        if self.lstBatchs.curselection():
            self.index = self.lstBatchs.curselection()[0]
            pk = self.dict_batchs.get(self.index)
            self.selected_batch = self.engine.get_selected('batchs','batch_id', pk)
            self.set_values(self.lstResults)

    def on_result_selected(self, event):

        if self.lstResults.curselection():
            self.index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(self.index)
            self.selected_result = self.engine.get_selected('results','result_id', pk)

    def on_batch_activated(self, event):

        if self.lstBatchs.curselection():
            self.obj = batch.Dialog(self,self.engine, self.index)
            self.obj.transient(self)
            self.obj.on_open(self.selected_test, self.selected_batch)

    def on_result_activated(self, event):

        if self.lstResults.curselection():
            self.obj = result.Dialog(self,self.engine,self.index)
            self.obj.transient(self)
            self.obj.on_open(self.selected_batch, self.selected_result)
            
    def on_add_batch(self,):

        if self.selected_test is not None:
            self.obj = batch.Dialog(self,self.engine,self.index)
            self.obj.transient(self)
            self.obj.on_open(self.selected_test)
        else:
            msg = "Please select a test."
            messagebox.showwarning(self.engine.title,msg)                    

        
    def on_add_result(self,):

        if self.selected_batch is not None:
            self.obj = result.Dialog(self,self.engine,self.index)
            self.obj.transient(self)
            self.obj.on_open(self.selected_batch)
            
        else:
            msg = "Please select a batch."
            messagebox.showwarning(self.engine.title,msg)                  

    def on_cancel(self, evt=None):
        self.destroy()
    
