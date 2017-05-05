#!/usr/bin/python
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------

from Tkinter import *
import tkMessageBox
import batch, result

class Dialog(Toplevel):     
    def __init__(self,parent,engine):
        Toplevel.__init__(self,)

        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
    
        self.selected_test = None
        self.selected_batch = None
        self.selected_result = None

        self.panel = Frame(self, bd=5, padx = 5, pady = 5)
        
        self.tests = LabelFrame(self.panel,text='Tests',padx = 5, pady = 5)      

        self.tests_scroll_bar = Scrollbar(self.tests,orient=VERTICAL)
        self.lstTests = Listbox(self.tests,
                                    relief=GROOVE,
                                    selectmode=BROWSE,
                                    bg='white',
                                    yscrollcommand=self.tests_scroll_bar.set,)
        self.lstTests.bind("<<ListboxSelect>>", self.on_selected_test)
        self.tests_scroll_bar.config(command=self.lstTests.yview)

        
        self.lstTests.pack(side=LEFT,fill=BOTH) 
        self.tests_scroll_bar.pack(fill=BOTH, expand=1)

        self.tests.pack(fill=BOTH, side=LEFT, padx=5, pady=5,)

        msg = '{:<20}{:<12}{:<10}{:<15}'.format('Batchs','Expirations','Target','SD')
        self.batchs = LabelFrame(self.panel,text= msg, padx = 5, pady = 5)      

        self.batchs_scroll_bar = Scrollbar(self.batchs,orient=VERTICAL)
        self.lstBatchs = Listbox(self.batchs,
                                    relief=GROOVE,
                                    width=40,
                                    selectmode=BROWSE,
                                    bg='white',
                                    yscrollcommand=self.batchs_scroll_bar.set,)
        self.lstBatchs.bind("<<ListboxSelect>>", self.on_selected_batch)
        self.lstBatchs.bind("<Double-Button-1>", self.on_batch_double_click)
        self.batchs_scroll_bar.config(command=self.lstTests.yview)

        
        self.lstBatchs.pack(side=LEFT,fill=BOTH, expand=1) 
        self.batchs_scroll_bar.pack(fill=BOTH, expand=1)

        self.batchs.pack(side=LEFT, fill=BOTH, padx = 5, pady = 5)

        s = '{:<15}{:<20}'.format('Recived','Result')
        self.results = LabelFrame(self.panel,text=s, padx = 5, pady = 5)      

        self.results_scroll_bar = Scrollbar(self.results,orient=VERTICAL)
        self.lstResults = Listbox(self.results,
                                    relief=GROOVE,
                                    selectmode=BROWSE,
                                    bg='white',
                                    yscrollcommand=self.results_scroll_bar.set,)
        self.lstResults.bind("<<ListboxSelect>>", self.on_selected_result)
        self.lstResults.bind("<Double-Button-1>", self.on_result_double_click)
        self.results_scroll_bar.config(command=self.lstTests.yview)

        
        self.lstResults.pack(side=LEFT,fill=BOTH, expand =1) 
        self.results_scroll_bar.pack(fill=BOTH, expand=1)

        self.results.pack(fill=BOTH, side=LEFT, padx = 5, pady = 5)

        self.buttons = Frame(self.panel, bd=5, padx = 5, pady = 5)
        
        self.btnBatch = Button(self.buttons, text="Batch", command=self.on_add_batch)
        self.btnBatch.pack(fill=X, padx=10, expand=1)

        self.btnResult = Button(self.buttons, text="Result", command=self.on_add_result)
        self.btnResult.pack(fill=X, padx=10, expand=1)

        self.btClose = Button(self.buttons, text="Close", command = self.on_cancel)
        self.btClose.pack(fill=X, padx=5, pady=5, expand=1)

        self.buttons.pack(fill=BOTH, side=LEFT)
        
        self.panel.pack(fill=BOTH, expand=1, padx=5, pady=5)

        
 
      
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
            
    def on_selected_test(self,event):

        self.index = self.lstTests.curselection()[0]
        pk = self.dict_tests.get(self.index)
        self.selected_test = self.engine.get_selected('tests','test_id', pk)

        self.set_values(self.lstBatchs)
       
        
    def on_selected_batch(self, event):

        self.index = self.lstBatchs.curselection()[0]
        pk = self.dict_batchs.get(self.index)
        self.selected_batch = self.engine.get_selected('batchs','batch_id', pk)

        self.set_values(self.lstResults)

    def on_selected_result(self, event):

        self.index = self.lstResults.curselection()[0]
        pk = self.dict_results.get(self.index)
        self.selected_result = self.engine.get_selected('results','result_id', pk)

    def on_batch_double_click(self, event):

        if self.lstBatchs.curselection():

            obj = batch.Dialog(self,self.selected_test,self.engine,self.index)
            obj.attributes("-topmost", True)
            obj.on_open(self.selected_batch)
            obj.wait_visibility()
            obj.grab_set()
            self.wait_window(obj)
            
        else:
            msg = "No batch selected."
            tkMessageBox.showwarning(self.engine.title,msg)                     

    def on_result_double_click(self, event):

        if self.lstResults.curselection():
            obj = result.Dialog(self,self.selected_batch,self.engine,self.index)
            obj.attributes("-topmost", True)
            obj.on_open(self.selected_result)
            obj.wait_visibility()
            obj.grab_set()
            self.wait_window(obj)
        else:
            msg = "No result selected."
            tkMessageBox.showwarning(self.engine.title,msg)


    def on_add_batch(self,):

        if self.selected_test is not None:
            obj = batch.Dialog(self,self.selected_test,self.engine,self.index)
            obj.attributes("-topmost", True)
            obj.on_open()
            obj.wait_visibility()
            obj.grab_set()
            self.wait_window(obj)

        else:
            msg = "Please select a test."
            messagebox.showwarning(self.engine.title,msg)                    

        
    def on_add_result(self,):

        if self.selected_batch is not None:
            obj = result.Dialog(self,self.selected_batch,self.engine,self.index)
            obj.attributes("-topmost", True)
            obj.on_open()
            obj.wait_visibility()
            obj.grab_set()
            self.wait_window(obj)

        else:
            msg = "Please select a batch."
            messagebox.showwarning(self.engine.title,msg)                  

             
    def on_selected(self,event):

        self.index = self.lstTests.curselection()[0]
        pk = self.dict_tests.get(self.index)
        self.selected_test = self.engine.get_selected('tests','test_id', pk)

    def on_cancel(self,):
        self.destroy()
    
