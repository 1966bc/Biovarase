""" This is the data module of Biovarase."""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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

class Widget(tk.Toplevel):     
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='data')

        self.parent = parent
        self.engine = kwargs['engine']
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.attributes('-topmost', True)
        self.minsize(800,400)
        self.data = tk.StringVar()
        self.objs = []
        self.init_ui()
        self.engine.center_me(self)
        
    def init_ui(self):
    
        f0 = self.engine.get_frame(self,8)

        f1 = tk.Frame(f0,)
        
        w = tk.LabelFrame(f1, text='Tests')
        self.cbTests =  ttk.Combobox(w)
        self.cbTests.bind("<<ComboboxSelected>>", self.on_selected_test)
        self.cbTests.pack(side=tk.TOP, fill=tk.X, expand=0)
        w.pack(side=tk.TOP, fill=tk.X, expand=0)
        
        w = tk.LabelFrame(f1, text='Batchs')
        cols = (["#0",'id','w',False,0,0],
                ["#1",'Batch','w',True,50,50],
                ["#2",'Expiration','w',True,50,50],
                ["#3",'Target','w',True,50,50],
                ["#4",'SD','w',True,50,50],)
        
        self.lstBatches = self.engine.get_tree(w, cols)
        self.lstBatches.bind("<<TreeviewSelect>>", self.on_selected_batch)
        self.lstBatches.bind("<Double-1>", self.on_batch_activated)

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

        cols = (["#0",'id','w',False,0,0],
                ["#1",'Recived','w',True,50,50],
                ["#2",'Result','w',True,50,50],)
        
        self.lstResults = self.engine.get_tree(f2, cols)
        self.lstResults.bind("<<TreeviewSelect>>", self.on_result_selected)
        self.lstResults.bind("<Double-1>", self.on_result_activated)
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        f2.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        
        w = tk.LabelFrame(self, relief=tk.GROOVE, bd=1, padx=5, pady=5,)    
        self.btnBatch = self.engine.get_button(w, "Batch")
        self.btnBatch.bind("<Button-1>", self.on_add_batch)
        self.btnResult = self.engine.get_button(w, "Result")
        self.btnResult.bind("<Button-1>", self.on_add_result)
        self.btnReset = self.engine.get_button(w, "Reset")
        self.btnReset.bind("<Button-1>", self.on_reset_database)
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

        self.lstBatches.tag_configure('is_enable', background=self.engine.get_rgb(211, 211, 211))

        for i in self.lstBatches.get_children():
            self.lstBatches.delete(i)
            
        for i in self.lstResults.get_children():
            self.lstResults.delete(i)
            
        msg = "Batch: None Results: 0"
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
        
        
        if rs:
            for i in rs:

                if i[5]!=1:
                    
                    self.lstBatches.insert('', tk.END,
                                           iid=i[0],
                                           text=i[0],
                                           values=(i[1],i[2],i[3],i[4]),
                                           tags = ('is_enable',))
                else:
                    self.lstBatches.insert('', tk.END,
                                           iid=i[0],
                                           text=i[0],
                                           values=(i[1],i[2],i[3],i[4]))                        
    
    def set_results(self,):

        for i in self.lstResults.get_children():
            self.lstResults.delete(i)

        self.lstResults.tag_configure('is_enable', background=self.engine.get_rgb(211, 211, 211))


        sql = "SELECT result_id,\
                      strftime('%d-%m-%Y', recived),\
                      ROUND(result,2),\
                      enable\
               FROM results\
               WHERE batch_id = ?\
               ORDER BY recived DESC"

        rs = self.engine.read(True, sql, (self.selected_batch[0],))
        msg = "Batch: {0} Results: {1}".format(self.selected_batch[2], len(rs))
        self.data.set(msg)

        if rs:
            for i in rs:
                if i[3]!=1:
                    
                    self.lstResults.insert('', tk.END,
                                           iid=i[0],
                                           text=i[0],
                                           values=(i[1],i[2]), tags = ('is_enable',))
                else:
                    self.lstResults.insert('', tk.END,
                                           iid=i[0],
                                           text=i[0],
                                           values=(i[1],i[2]))

    def on_selected_test(self,event):

        if self.cbTests.current()!=-1:
            index = self.cbTests.current()
            pk = self.dict_tests[index]
            self.selected_test = self.engine.get_selected('lst_tests','test_id', pk)
            self.set_batches()
                   
    def on_selected_batch(self, event):

        if self.lstBatches.focus():
            pk = int(self.lstBatches.item(self.lstBatches.focus())['text'])
            self.selected_batch = self.engine.get_selected('batches','batch_id', pk)
            self.set_results()

    def on_result_selected(self, event):

         if self.lstResults.focus():
            pk = int(self.lstResults.item(self.lstResults.focus())['text'])
            self.selected_result = self.engine.get_selected('results','result_id', pk)
      

    def on_batch_activated(self, event):

        if self.lstBatches.focus():
            item_iid = self.lstBatches.selection()
            obj = batch.Widget(self, engine=self.engine, index=item_iid)
            obj.on_open(self.selected_test, self.selected_batch)
            self.objs.append(obj)
             
    
    def on_result_activated(self, event):

        if self.lstResults.focus():
            item_iid = self.lstResults.selection()
            obj = result.Widget(self, engine=self.engine, index=item_iid)
            obj.on_open(self.selected_test,
                             self.selected_batch,
                             self.selected_result)
            self.objs.append(obj)
               
    def on_add_batch(self,evt):

        if self.cbTests.current()!=-1:
            obj = batch.Widget(self, engine=self.engine, index=None)
            obj.on_open(self.selected_test)
            self.objs.append(obj)
        else:
            msg = "Please select a test."
            messagebox.showwarning(self.engine.title, msg, parent=self)                    

        
    def on_add_result(self,evt):

        if self.lstBatches.focus():
            obj = result.Widget(self, engine=self.engine, index=None)
            obj.on_open(self.selected_test, self.selected_batch)
            self.objs.append(obj)
            
        else:
            msg = "Please select a batch."
            messagebox.showwarning(self.engine.title, msg, parent=self)

    def on_reset_database(self, evt):

        msg = "You are about to delete the entire database.\nAre you sure? "

        if messagebox.askyesno(self.engine.title, msg, default='no', parent=self) == True:

            self.engine.dump_db()
            
            sql = ("DELETE FROM tests",
                   "DELETE FROM batches",
                   "DELETE FROM results",
                   "DELETE FROM rejections",)

            for statement in sql:
                self.engine.write(statement,())
            
            self.parent.on_reset()
            self.on_cancel()  
        else:
            messagebox.showinfo(self.engine.title, self.engine.abort, parent=self)              

    def on_cancel(self, evt=None):
        for obj in self.objs:
            obj.destroy()
        self.destroy()
    
