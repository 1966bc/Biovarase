# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="goal")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)
        self.vcmd_int = self.nametowidget(".").engine.get_validate_integer(self)

       
        self.cvw = tk.DoubleVar()
        self.cvb = tk.DoubleVar()
        self.imp = tk.DoubleVar()
        self.bias = tk.DoubleVar()
        self.teap005 = tk.DoubleVar()
        self.teap001 = tk.DoubleVar()
        self.to_export = tk.BooleanVar()
        self.status = tk.BooleanVar()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        r += 1
        ttk.Label(frm_left, text="cvw:").grid(row=r, sticky=tk.W)
        self.txCvw = ttk.Entry(frm_left,
                               width=8,
                               justify=tk.CENTER,
                               validate='key',
                               validatecommand=self.vcmd,
                               textvariable=self.cvw)
        self.txCvw.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="cvb:").grid(row=r, sticky=tk.W)
        self.txCvb = ttk.Entry(frm_left,
                               width=8,
                               justify=tk.CENTER,
                               validate='key',
                               validatecommand=self.vcmd,
                               textvariable=self.cvb)
        self.txCvb.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Imp %:").grid(row=r, sticky=tk.W)
        self.txImp = ttk.Entry(frm_left,
                               width=8,
                               justify=tk.CENTER,
                               validate='key',
                               validatecommand=self.vcmd,
                               textvariable=self.imp)
        self.txImp.grid(row=r, column=c, sticky=tk.W, **paddings)


        r += 1
        ttk.Label(frm_left, text="Bias %:").grid(row=r, sticky=tk.W)
        self.txBias = ttk.Entry(frm_left,
                                width=8,
                                justify=tk.CENTER,
                                validate='key',
                                validatecommand=self.vcmd,
                                textvariable=self.bias)
        self.txBias.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="TEa % p<0.05:").grid(row=r, sticky=tk.W)
        self.txTeaP005 = ttk.Entry(frm_left,
                                   width=8,
                                   justify=tk.CENTER,
                                   validate='key',
                                   validatecommand=self.vcmd,
                                   textvariable=self.teap005)
        self.txTeaP005.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="TEa % p<0.01:").grid(row=r, sticky=tk.W)
        self.txTeaP002 = ttk.Entry(frm_left,
                                   width=8,
                                   justify=tk.CENTER,
                                   validate='key',
                                   validatecommand=self.vcmd,
                                   textvariable=self.teap001)
        self.txTeaP002.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="To export:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.to_export,)
        chk.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status)
        chk.grid(row=r, column=c, sticky=tk.EW, **paddings)

        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)
        
        r = 0
        c = 0
        btn_save = ttk.Button(frm_buttons, style="App.TButton", text="Save", underline=0, command=self.on_save,)
        self.bind("<Alt-s>", self.on_save)
        btn_save.grid(row=r, column=c, sticky=tk.EW, **paddings)
  
        r += 1
        btn_cancel = ttk.Button(frm_buttons, style="App.TButton", text="Cancel", underline=0, command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn_cancel.grid(row=r, column=c, sticky=tk.EW, **paddings)

    def on_open(self, selected_test_method):

        self.selected_test_method = selected_test_method

        sql = "SELECT * FROM goals WHERE test_method_id =?"
        args = (selected_test_method[0],)
        self.selected_goal = self.nametowidget(".").engine.read(False, sql, args)
        
        if self.selected_goal is not None:
            msg = "Update analytical goal for {0}".format(self.parent.selected_test[1])
            self.set_values()
        else:
            msg = "Insert analytical goal for {0}".format(self.parent.selected_test[1])
            self.status.set(1)

        self.title(msg)
        self.txCvw.focus()
         
    def set_values(self,):
        
        self.cvw.set(self.selected_goal[2])
        self.cvb.set(self.selected_goal[3])
        self.imp.set(self.selected_goal[4])
        self.bias.set(self.selected_goal[5])
        self.teap005.set(self.selected_goal[6])
        self.teap001.set(self.selected_goal[7])
        self.to_export.set(self.selected_goal[8])
        self.status.set(self.selected_goal[9])


    def get_values(self,):

        return [self.selected_test_method[0],
                self.cvw.get(),
                self.cvb.get(),
                self.imp.get(),
                self.bias.get(),
                self.teap005.get(),
                self.teap001.get(),
                self.to_export.get(),
                self.status.get()]
        

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(), self.nametowidget(".").engine.ask_to_save, parent=self) == True:

            args = self.get_values()

            if self.selected_goal is not None:

                sql = self.nametowidget(".").engine.get_update_sql("goals", "goal_id")

                args.append(self.selected_goal[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql("goals", len(args))
            
            self.nametowidget(".").engine.write(sql, args)
 
            self.on_cancel()

    def on_cancel(self, evt=None):
        self.destroy()
