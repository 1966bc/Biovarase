#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox

import frames.batch
import frames.result

class Dialog(Toplevel):     
    def __init__(self,parent, engine):
        super().__init__(name='batchs')

        #self.resizable(0,0)
        #self.geometry("{0}x{1}+0+0".format(1200, 600))
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = engine
        
        self.enable =  BooleanVar()
        self.obj = None
        self.selected_data = StringVar()
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
    
        f0 = self.engine.get_frame(self)
        
        w_tests = self.engine.get_frame(self)
        
        Label(w_tests,font='Times 12 bold italic', foreground="blue", textvariable = self.selected_data).pack()
        
        w = LabelFrame(w_tests,text=  "Tests", padx = 5, pady = 5)
        self.lstTests = self.engine.get_listbox(w,)
        self.lstTests.bind("<<ListboxSelect>>", self.on_test_selected)
        w.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)
        w_tests.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)

        w_batchs = self.engine.get_frame(self)
        s = '{0:8}{1:>12}{2:>15}{3:>12}'.format('Batchs','Expirations','Target','SD')
        w = LabelFrame(w_batchs,text= s, padx = 5, pady = 5)
        self.lstBatches = self.engine.get_listbox(w,)
        self.lstBatches.bind("<<ListboxSelect>>", self.on_batch_selected)
        self.lstBatches.bind("<Double-Button-1>", self.on_batch_activated)
        w.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)
        w_batchs.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)

        
        w_results = self.engine.get_frame(self)
        s = '{:<15}{:<20}'.format('Recived','Result')
        w = LabelFrame(w_results,text=s, padx = 5, pady = 5)
        self.lstResults = self.engine.get_listbox(w)
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
        
        f0.pack(fill=BOTH,padx=5, pady=5, expand =1)

    def on_open(self,):

        self.set_tests()
     
        self.title("Batchs and results management")

        self.selected_data.set('Test')

    def set_tests(self):

        sql = "SELECT tests.test_id,tests.test||' '||samples.sample\
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
                self.dict_tests[index]=i[0]
                index+=1
        
    def set_batches(self,):

        self.lstBatches.delete(0, END)
        self.lstResults.delete(0, END)

        index = 0
        self.dict_batchs={}
        sql = "SELECT batch_id, batch,strftime('%d-%m-%Y', expiration), target, sd, enable FROM batchs WHERE test_id = ?"
        rs = self.engine.read(True, sql, (self.selected_test[0],))
        
        if rs:
            for i in rs:
                
                s = '{0:8}{1:>10}{2:>10}{3:>10}'.format(i[1],i[2],i[3],i[4])
                self.lstBatches.insert(END, (s))
                if i[5] !=1:
                    self.lstBatches.itemconfig(index, {'bg':'gray'})
                self.dict_batchs[index]=i[0]
                index+=1

    def set_results(self,):

        self.lstResults.delete(0, END)
        index = 0
        self.dict_results={}
        sql = "SELECT result_id,\
                      ROUND(result,2),\
                      strftime('%d-%m-%Y', recived),\
                      enable\
               FROM results\
               WHERE batch_id = ?\
               ORDER BY recived DESC"
        rs = self.engine.read(True, sql, (self.selected_batch[0],))
        
        if rs:
            for i in rs:
                s = '{0:^10}{1:^10}'.format(i[2],i[1])
                self.lstResults.insert(END, (s))
                if i[3] != 1:
                    self.lstResults.itemconfig(index, {'bg':'gray'})
                self.dict_results[index]=i[0]
                index+=1

            
    def on_test_selected(self,evt):

        if self.lstTests.curselection():
            index = self.lstTests.curselection()[0]
            pk = self.dict_tests.get(index)
            self.selected_test = self.engine.get_selected('lst_tests','test_id', pk)
            self.selected_data.set(self.lstTests.get(index))
            self.set_batches()
       
    def on_batch_selected(self, evt):

        if self.lstBatches.curselection():
            index = self.lstBatches.curselection()[0]
            pk = self.dict_batchs.get(index)
            self.selected_batch = self.engine.get_selected('batchs','batch_id', pk)
            self.set_results()

    def on_batch_activated(self, evt):

        if self.lstBatches.curselection():
            index = self.lstBatches.curselection()[0]
            self.obj = frames.batch.Dialog(self,self.engine, index)
            self.obj.on_open(self.selected_test, self.selected_batch)

    def on_add_batch(self, evt):

        if self.lstTests.curselection():
            self.obj = frames.batch.Dialog(self,self.engine,)
            self.obj.transient(self)
            self.obj.on_open(self.selected_test)

        else:
            msg = "Attention please.\nBefore add a batch you must select a test."
            messagebox.showinfo(self.engine.title, msg)                        

    def on_result_selected(self, evt):

        if self.lstResults.curselection():
            index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(index)
            self.selected_result = self.engine.get_selected('results','result_id', pk)
            
    def on_result_activated(self, evt):

        if self.lstResults.curselection():
            index = self.lstResults.curselection()[0]
            self.obj = frames.result.Dialog(self,self.engine, index)
            self.obj.on_open(self.selected_test, self.selected_batch, self.selected_result)

    def on_add_result(self, evt):

        if self.lstBatches.curselection():
            self.obj = frames.result.Dialog(self, self.engine,)
            self.obj.on_open(self.selected_test, self.selected_batch)
            
        else:
            msg = "Attention please.\nBefore add a result you must select a batch."
            messagebox.showwarning(self.engine.title, msg)             

                    
    def on_cancel(self, evt=None):

        """force closing of the childs...
        """     
        
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
