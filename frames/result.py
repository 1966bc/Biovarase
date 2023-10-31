# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
import os
import sys
import inspect
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from calendarium import Calendarium



class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="result")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.attributes('-topmost', True)
        self.resizable(0, 0)

        self.test = tk.StringVar()
        self.batch = tk.StringVar()
        self.description = tk.StringVar()
        self.workstation = tk.StringVar()
        self.result = tk.DoubleVar()
        self.status = tk.BooleanVar()

        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)
        self.nametowidget(".").engine.set_instance(self, 1)
       

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        ttk.Label(frm_left, text="Test:").grid(row=r, sticky=tk.W)
        ttk.Label(frm_left,
                  style="Data.TLabel",
                  textvariable=self.test).grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="Batch:").grid(row=r, sticky=tk.W)
        ttk.Label(frm_left,
                  style="Data.TLabel",
                  textvariable=self.batch).grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)


        r += 1
        ttk.Label(frm_left, text="Descrption:").grid(row=r, sticky=tk.W)
        ttk.Label(frm_left,
                  style="Data.TLabel",
                  textvariable=self.description).grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)


        r += 1
        ttk.Label(frm_left, text="Workstation:").grid(row=r, sticky=tk.W)
        ttk.Label(frm_left,
                  style="Data.TLabel",
                  textvariable=self.workstation).grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)
        
        r += 1
        ttk.Label(frm_left, text="Result:").grid(row=r, sticky=tk.W)
        self.txtResult = ttk.Entry(frm_left,
                                   width=8,
                                   justify=tk.CENTER,
                                   validate="key",
                                   validatecommand=self.vcmd,
                                   textvariable=self.result)
        self.txtResult.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="Recived:").grid(row=r, sticky=tk.N+tk.W)

        self.recived_date = Calendarium(self, "")
        self.recived_date.get_calendarium(frm_left, r, c)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        self.ckStatus = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status,)
        self.ckStatus.grid(row=r, column=c, sticky=tk.W)

        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)
        
        r = 0
        c = 0
        btn = ttk.Button(frm_buttons, style="App.TButton", text="Save", underline=0, command=self.on_save,)
        self.bind("<Alt-s>", self.on_save)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        if self.nametowidget(".").engine.log_user[5] <2:

            if self.index is not None:
                r += 1
                btn = ttk.Button(frm_buttons, style="App.TButton", text="Delete", underline=0, command=self.on_delete)
                self.bind("<Alt-c>", self.on_cancel)
                btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        btn = ttk.Button(frm_buttons, style="App.TButton", text="Cancel", underline=0, command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)
         
    def on_open(self, selected_test_method, selected_batch, selected_workstation, selected_result=None):

        self.selected_test_method = selected_test_method
        self.selected_workstation = selected_workstation
        self.selected_batch = selected_batch
        self.selected_workstation = selected_workstation
        self.test.set(self.nametowidget(".").engine.get_test_name(selected_test_method[1]))
        self.batch.set(self.selected_batch[4])
        self.description.set(self.selected_batch[8])
        self.workstation.set(self.selected_workstation[3])


        if self.index is not None:
            self.selected_result = selected_result
            msg = "Update {0} ".format(self.winfo_name().capitalize())
            self.set_values()
            self.txtResult.focus()
        else:
            msg = "Add {0} ".format(self.winfo_name().capitalize())
                                          
            self.status.set(1)
            self.result.set('')
            self.recived_date.set_today()
            self.txtResult.focus()
            
        self.title(msg)

    def on_selected_workstation(self, evt):

        if self.cbWorkstations.current() != -1:

            index = self.cbWorkstations.current()
            pk = self.dict_workstations[index]
            self.selected_workstation = self.nametowidget(".").engine.get_selected("workstations", "workstation_id", pk)
        
    def get_values(self,):
       
        if self.index is not None:

            run_number = self.selected_result[2]
            is_delete = self.selected_result[7]

        else:
            run_number = 0
            is_delete = 0

        args = [self.selected_batch[0],
                run_number,
                self.selected_workstation[0],
                round(self.result.get(),3),
                self.recived_date.get_timestamp(),
                self.status.get(),
                is_delete,
                self.nametowidget(".").engine.get_log_time(),
                self.nametowidget(".").engine.get_log_id(),
                self.nametowidget(".").engine.get_log_ip()]
        
        return args

    def set_values(self,):
        
        try:
            key = next(key for key, value in self.dict_workstations.items() 
            if value == self.selected_result[3])
            self.cbWorkstations.current(key)
        except:
            pass

        try:
            self.recived_date.year.set(int(self.selected_result[5].year))
            self.recived_date.month.set(int(self.selected_result[5].month))
            self.recived_date.day.set(int(self.selected_result[5].day))
            
        except:
             nametowidget(".").on_log(inspect.stack()[0][3],
                                      sys.exc_info()[1],
                                      sys.exc_info()[0],
                                      sys.modules[__name__])
    
        self.result.set(round(self.selected_result[4],3))
        self.status.set(self.selected_result[6])
        
    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return
        if self.recived_date.get_date(self) == False: return
        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:
                sql = self.nametowidget(".").engine.get_update_sql("results", "result_id")
                args.append(self.selected_result[0])

            else:
                sql = self.nametowidget(".").engine.get_insert_sql("results", len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)

            self.update_results_lists()

            self.set_index(last_id)
            
            self.on_cancel()

    def update_results_lists(self):

        try:
            if self.parent.winfo_name() == "data":
                self.nametowidget(".").nametowidget("data").set_results()
                
            self.nametowidget(".main").set_results()
        except:
            nametowidget(".").on_log(inspect.stack()[0][3],
                                     sys.exc_info()[1],
                                     sys.exc_info()[0], sys.modules[__name__])

    def set_index(self, last_id):

        if self.index is not None:
            idx = self.index
        else:
            idx = list(self.parent.dict_results.keys())[list(self.parent.dict_results.values()).index(last_id)]

        self.parent.lstResults.selection_set(idx)
        self.parent.lstResults.see(idx)            
             
            
    def on_delete(self, evt=None):

        if self.nametowidget(".").engine.log_user[5] ==2:
            msg = self.nametowidget(".").engine.user_not_enable
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

        else:            

            if self.index is not None:
                if messagebox.askyesno(self.nametowidget(".").title(),
                                       self.nametowidget(".").engine.delete,
                                       parent=self) == True:
                    
                    sql = "DELETE FROM results WHERE result_id =?;"
                    args = (self.selected_result[0],)
                    self.nametowidget(".").engine.write(sql, args)
                    
                    self.update_results_lists()
                    
                    self.on_cancel()

                else:
                    messagebox.showinfo(self.nametowidget(".").title(), 
                                        self.nametowidget(".").engine.abort, 
                                        parent=self)

    def on_cancel(self, evt=None):
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()
    
