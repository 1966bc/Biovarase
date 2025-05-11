# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
#-----------------------------------------------------------------------------
import sys
import inspect
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from calendarium import Calendarium

class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="methods_comp_result")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.attributes('-topmost', True)
        self.resizable(0, 0)

        self.result_y = tk.DoubleVar()
        self.result_x = tk.DoubleVar()
        self.recived_date = Calendarium(self, "")
        self.status = tk.BooleanVar()

        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)
        self.vcmd_int = self.nametowidget(".").engine.get_validate_integer(self)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.init_ui()
        self.nametowidget(".").engine.center_window_on_screen(self)
        self.nametowidget(".").engine.set_instance(self, 1)
       
    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        ttk.Label(frm_left, text="Test(Y):").grid(row=r, sticky=tk.W)
        self.txtTestY = ttk.Entry(frm_left,
                                   width=8,
                                   justify=tk.CENTER,
                                   validate="key",
                                   validatecommand=self.vcmd,
                                   textvariable=self.result_y)
        self.txtTestY.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)


        r += 1
        ttk.Label(frm_left, text="Comp(X):").grid(row=r, sticky=tk.W)
        self.txtCompX = ttk.Entry(frm_left,
                                   width=8,
                                   justify=tk.CENTER,
                                   validate="key",
                                   validatecommand=self.vcmd,
                                   textvariable=self.result_x)
        self.txtCompX.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="Recived:").grid(row=r, sticky=tk.N+tk.W)
        self.recived_date.get_calendarium(frm_left, r, c)

        if self.index is not None:
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
         
    def on_open(self,):

        if self.index is not None:
            msg = "Update data {0}".format(self.parent.test[0])
            self.set_values()
        else:
            msg = "Add data {0}".format(self.parent.test[0])
            self.result_y.set("")
            self.result_x.set("")
            self.recived_date.set_today()
            self.status.set(1)
        
        self.txtTestY.focus()    
        self.title(msg)
        
    def get_values(self,):
       
        args = [self.parent.selected_experiment[0],
                round(self.result_y.get(),2),
                round(self.result_x.get(),2),
                self.recived_date.get_timestamp(),
                self.status.get(),
                self.nametowidget(".").engine.get_log_time(),
                self.nametowidget(".").engine.get_log_id(),
                self.nametowidget(".").engine.get_log_ip()]
        
        return args

    def set_values(self,):
        
        self.result_y.set(round(self.parent.selected_result[2],2))
        self.result_x.set(round(self.parent.selected_result[3],2))
        try:
            self.recived_date.year.set(int(self.parent.selected_result[4].year))
            self.recived_date.month.set(int(self.parent.selected_result[4].month))
            self.recived_date.day.set(int(self.parent.selected_result[4].day))
            
        except:
            self.nametowidget(".").on_log(inspect.stack()[0][3],
                                      sys.exc_info()[1],
                                      sys.exc_info()[0],
                                      sys.modules[__name__])
        self.status.set(self.parent.selected_result[5])
        
    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return
        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:
                sql = self.nametowidget(".").engine.get_update_sql("methods_comp_results", "result_id")
                args.append(self.parent.selected_result[0])

            else:
                sql = self.nametowidget(".").engine.get_insert_sql("methods_comp_results", len(args))

            self.nametowidget(".").engine.write(sql, args)

            self.parent.set_results()

            self.on_cancel()

            
    def on_delete(self, evt=None):

        if self.nametowidget(".").engine.log_user[5] ==2:
            msg = self.nametowidget(".").engine.user_not_enable
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

        else:            

            if self.index is not None:
                if messagebox.askyesno(self.nametowidget(".").title(),
                                       self.nametowidget(".").engine.ask_to_delete,
                                       parent=self) == True:
                    
                    sql = "DELETE FROM methods_comp_results WHERE result_id =?;"
                    args = (self.parent.selected_result[0],)
                    self.nametowidget(".").engine.write(sql, args)
                    
                    self.parent.set_results()
                    
                    self.on_cancel()

                else:
                    messagebox.showinfo(self.nametowidget(".").title(), 
                                        self.nametowidget(".").engine.abort, 
                                        parent=self)

    def on_cancel(self, evt=None):
        self.nametowidget(".").engine.set_instance(self, 0)
        self.destroy()
    
