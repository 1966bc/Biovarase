""" This is the data module of Biovarase."""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import frames.batch as batch
import frames.result as result

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"

class Dialog(tk.Toplevel):     
    def __init__(self,parent, engine):
        super().__init__(name='data')

        self.parent = parent
        self.engine = engine
        self.data = tk.StringVar()
        self.obj = None
        self.init_ui()
        
    def init_ui(self):
    
        f0 = self.engine.get_frame(self)

        f1 = tk.Frame(f0,)
        
        w = tk.LabelFrame(f1, text='Tests')
        self.cbTests =  ttk.Combobox(w)
        self.cbTests.bind("<<ComboboxSelected>>", self.on_selected_test)
        self.cbTests.pack(side=tk.TOP, fill=tk.X, expand=0)
        w.pack(side=tk.TOP, fill=tk.X, expand=0)
        
        w = tk.LabelFrame(f1, text='Batchs')
        self.lstBatches = self.engine.get_listbox(w, height=5)
        self.lstBatches.bind("<<ListboxSelect>>", self.on_selected_batch)
        self.lstBatches.bind("<Double-Button-1>", self.on_batch_activated)
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        f2 = tk.Frame(f0,)
        tk.Label(f2,
                 font="TkFixedFont",
                 anchor=tk.W,
                 textvariable=self.data,
                 padx=5,
                 pady=5).pack(side=tk.TOP,
                              fill=tk.X,
                              expand=0)
        
        self.lstResults = self.engine.get_listbox(f2,)
        self.lstResults.bind("<<ListboxSelect>>", self.on_result_selected)
        self.lstResults.bind("<Double-Button-1>", self.on_result_activated)
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        f2.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        
        w = tk.LabelFrame(self, relief=tk.GROOVE, bd=1, padx=5, pady=5,)    
        self.btnBatch = self.engine.get_button(w, "Batch")
        self.btnBatch.bind("<Button-1>", self.on_add_batch)
        self.btnResult = self.engine.get_button(w, "Result")
        self.btnResult.bind("<Button-1>", self.on_add_result)
        self.btClose = self.engine.get_button(w, "Close")
        self.btClose.bind("<Button-1>", self.on_cancel)
        w.pack(fill=tk.BOTH, side=tk.RIGHT)
        
        f0.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

    def on_open(self,):

        msg = "Batch: %s Results: %s"%("None","0")
        self.data.set(msg)

        self.set_tests()
     
        self.title("Batches and Results Management")
   
    def set_tests(self):
        
        sql = "SELECT * FROM lst_tests"
    
        rs = self.engine.read(True, sql, ())
        index = 0
        self.dict_tests = {}
        voices = []

        for i in rs:
            self.dict_tests[index]=i[0]
            index+=1
            voices.append(i[1])

        self.cbTests['values']=voices   
        

    def set_batches(self,):

        self.lstBatches.delete(0, tk.END)
        self.lstResults.delete(0, tk.END)
        msg = "Batch: %s Results: %s"%("None","0")
        self.data.set(msg)

        sql = "SELECT batch_id,\
                      batch,\
                      strftime('%d-%m-%Y', expiration),\
                      target,\
                      sd,\
                      enable\
               FROM batches WHERE test_id = ?\
               ORDER BY expiration DESC"
        
        
        rs = self.engine.read(True, sql, (self.selected_test[0],))
        index = 0
        self.dict_batchs = {}
        
        if rs:
            for i in rs:
                try:
                    s = '{0:12}{1:16}{2:16}{3:16}'.format(i[1],i[2],i[3],i[4])
                    self.lstBatches.insert(tk.END, (s))
                    if i[5] !=1:
                        self.lstBatches.itemconfig(index, {'bg':'gray'})
                    self.dict_batchs[index]=i[0]
                    index +=1
                except:
                    print(inspect.stack()[0][3])
                    print (i)
                    print (sys.exc_info()[0])
                    print (sys.exc_info()[1])
                    print (sys.exc_info()[2])
                        
    
    def set_results(self,):

        self.lstResults.delete(0, tk.END)

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
        msg = "Batch: %s Results: %s"%(self.selected_batch[2], len(rs))
        self.data.set(msg)

        if rs:
            
            for i in rs:
                s = '{0:10}{1:10}'.format(i[2],i[1])
                self.lstResults.insert(tk.END, (s))
                if i[3] != 1:
                    self.lstResults.itemconfig(index, {'bg':'gray'})
                self.dict_results[index]=i[0]
                index+=1
        
            

    def on_selected_test(self,event):

        if self.cbTests.current()!=-1:
            index = self.cbTests.current()
            pk = self.dict_tests[index]
            self.selected_test = self.engine.get_selected('lst_tests','test_id', pk)
            self.set_batches()
                   
    def on_selected_batch(self, event):

        if self.lstBatches.curselection():
            index = self.lstBatches.curselection()[0]
            pk = self.dict_batchs.get(index)
            self.selected_batch = self.engine.get_selected('batches','batch_id', pk)
            self.set_results()

    def on_result_selected(self, event):

        if self.lstResults.curselection():
            index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(index)
            self.selected_result = self.engine.get_selected('results','result_id', pk)

    def on_batch_activated(self, event):

         if self.lstBatches.curselection():
            index = self.lstBatches.curselection()[0]
            self.obj = batch.Dialog(self,self.engine, index)
            self.obj.on_open(self.selected_test, self.selected_batch)

    
    def on_result_activated(self, event):

        if self.lstResults.curselection():
            index = self.lstResults.curselection()[0]
            self.obj = result.Dialog(self,self.engine, index)
            self.obj.on_open(self.selected_test,
                             self.selected_batch,
                             self.selected_result)

    def on_add_batch(self,evt):

        if self.selected_test is not None:
            self.obj = batch.Dialog(self,self.engine,)
            self.obj.transient(self)
            self.obj.on_open(self.selected_test)
        else:
            msg = "Please select a test."
            messagebox.showwarning(self.engine.title,msg)                    

        
    def on_add_result(self,evt):

        if self.selected_batch is not None:
            self.obj = result.Dialog(self, self.engine,)
            self.obj.transient(self)
            self.obj.on_open(self.selected_test, self.selected_batch)
            
        else:
            msg = "Please select a batch."
            messagebox.showwarning(self.engine.title,msg)                  

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
    
