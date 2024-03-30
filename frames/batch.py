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
        super().__init__(name="batch")
 
        self.parent = parent
        self.index = index
        #self.transient(parent)
        self.attributes('-topmost', True)
        self.resizable(0, 0)

        self.lot_number = tk.StringVar()
        self.description = tk.StringVar()

        self.lot_number.trace("w", lambda x, y, z,
                        c=self.nametowidget(".").engine.get_lot_length(),
                        v=self.lot_number: self.nametowidget(".").engine.limit_chars(c, v, x, y, z))
        
        self.description.trace("w", lambda x, y, z,
                        c=self.nametowidget(".").engine.get_batch_length(),
                        v=self.description: self.nametowidget(".").engine.limit_chars(c, v, x, y, z))
        
        self.target = tk.DoubleVar()
        self.sd = tk.DoubleVar()
        self.lower = tk.DoubleVar()
        self.upper = tk.DoubleVar()
        self.to_compute = tk.IntVar()
        self.ranck = tk.IntVar()
        self.status = tk.BooleanVar()
        self.set_remeber_batch_data = tk.BooleanVar()
        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)
        self.vcmd_int = self.nametowidget(".").engine.get_validate_integer(self)
        self.lower.trace("w", lambda x, y, z, c=16, v=self.lower: self.on_compute_sd(c, v, x, y, z))
        self.upper.trace("w", lambda x, y, z, c=16, v=self.upper: self.on_compute_sd(c, v, x, y, z))

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
        ttk.Label(frm_left, text="Control:").grid(row=r, sticky=tk.W)
        self.cbControls = ttk.Combobox(frm_left,)
        self.cbControls.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Workstations:").grid(row=r, sticky=tk.W)
        self.cbWorkstations = ttk.Combobox(frm_left,)
        self.cbWorkstations.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Lot:").grid(row=r, sticky=tk.W)
        self.txLotNumber = ttk.Entry(frm_left, textvariable=self.lot_number)
        self.txLotNumber.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Description:").grid(row=r, sticky=tk.W)
        self.txDescription = ttk.Entry(frm_left, textvariable=self.description)
        self.txDescription.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Expiration:").grid(row=r, sticky=tk.N+tk.W)
        self.expiration_date = Calendarium(self, "")
        self.expiration_date.get_calendarium(frm_left, r, c)

        r += 1
        ttk.Label(frm_left, text="Target:").grid(row=r, sticky=tk.W)
        self.txtTarget = ttk.Entry(frm_left,
                                   width=8,
                                   justify=tk.CENTER,
                                   validate='key',
                                   validatecommand=self.vcmd,
                                   textvariable=self.target)
        self.txtTarget.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Lower:").grid(row=r, sticky=tk.W)
        self.txtLower = ttk.Entry(frm_left,
                                  width=8,
                                  justify=tk.CENTER,
                                  validate='key',
                                  validatecommand=self.vcmd,
                                  textvariable=self.lower,
                                  state=tk.DISABLED)
        self.txtLower.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Upper:").grid(row=r, sticky=tk.W)
        self.txtUpper = ttk.Entry(frm_left,
                                  width=8,
                                  justify=tk.CENTER,
                                  validate='key',
                                  validatecommand=self.vcmd,
                                  textvariable=self.upper,
                                  state=tk.DISABLED)
        self.txtUpper.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="SD:").grid(row=r, sticky=tk.W)
        ent_sd = ttk.Entry(frm_left, width=8, justify=tk.CENTER,
                           validate='key', validatecommand=self.vcmd,
                           textvariable=self.sd)
        ent_sd.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Ranck:").grid(row=r, sticky=tk.W)
        ent_ranck= ttk.Entry(frm_left,
                               width=8,
                               justify=tk.CENTER,
                               validate="key",
                               validatecommand=self.vcmd_int,
                               textvariable=self.ranck)
        ent_ranck.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        ttk.Checkbutton(frm_left,
                        onvalue=1,
                        offvalue=0,
                        variable=self.status,).grid(row=r,
                                                    column=c,
                                                    sticky=tk.W)

        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)

        r = 0
        c = 0
        btn = ttk.Button(frm_buttons, style="App.TButton",
                         text="Save", underline=0,
                         command=self.on_save,)
        self.bind("<Alt-s>", self.on_save)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        btn = ttk.Button(frm_buttons, style="App.TButton",
                         text="Cancel", underline=0,
                         command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r +=1 
        ttk.Checkbutton(frm_buttons,
                        text = "Remember data",
                        onvalue=1,
                        offvalue=0,
                        variable=self.set_remeber_batch_data,).grid(row=r,
                                                    column=c,
                                                    sticky=tk.W)

        r += 1
        frm_sd = ttk.LabelFrame(frm_buttons, style="App.TLabelframe", text="SD mode", )
        frm_sd.grid(row=r, column=c, rowspan=4, sticky=tk.NW)

        voices = ["Manual", "Computed",]
        for index, text in enumerate(voices):
            ttk.Radiobutton(frm_sd,
                            style="App.TRadiobutton",
                            text=text,
                            variable=self.to_compute,
                            command=self.on_set_compute,
                            value=index,).grid(row=r, column=c, sticky=tk.EW, **paddings)
            r += 1       

    def on_open(self, selected_test_method, selected_workstation, selected_batch=None):

        self.workstation_section_id = selected_workstation[5]

        self.set_remeber_batch_data.set(self.nametowidget(".").engine.get_remeber_batch_data())

        self.set_controls()
        self.set_workstations()
        self.set_workstation(selected_workstation)

        sql = "SELECT * FROM tests WHERE test_id =?;"
        args = (selected_test_method[1],)
        self.selected_test = self.nametowidget(".").engine.read(False, sql, args)
        self.selected_test_method = selected_test_method

        if self.index is not None:
            self.selected_batch = selected_batch
            msg = "Update {0} {1} for {2}".format(self.winfo_name().capitalize(), self.selected_batch[4], self.selected_test[1])
            self.set_values()
            self.cbControls.focus()
        else:
            msg = "Insert {0} for {1}".format(self.winfo_name().capitalize(), self.selected_test[1])

            if self.set_remeber_batch_data.get()== True:
                
                if self.nametowidget(".").engine.batch_remembers is not None:

                    try:
                        key = next(key for key, value in self.dict_controls.items() if value == self.nametowidget(".").engine.batch_remembers[0])
                        self.cbControls.current(key)
                    except:
                        pass
                    
                    self.lot_number.set(self.nametowidget(".").engine.batch_remembers[3])
                    self.description.set(self.nametowidget(".").engine.batch_remembers[7])
                    self.expiration_date.year.set(int(self.nametowidget(".").engine.batch_remembers[4].year))
                    self.expiration_date.month.set(int(self.nametowidget(".").engine.batch_remembers[4].month))
                    self.expiration_date.day.set(int(self.nametowidget(".").engine.batch_remembers[4].day))
                else:
                    self.expiration_date.set_today()
                    self.cbControls.focus()
                    
            else:
                self.expiration_date.set_today()
                self.cbControls.focus()

            self.status.set(1)
            self.to_compute.set(1)
            self.on_set_compute()

        self.title(msg)
        
    def set_controls(self):

        index = 0
        self.dict_controls = {}
        values = []

        sql = "SELECT control_id, description\
               FROM controls\
               WHERE status =1\
               ORDER BY description ASC;"

        rs = self.nametowidget(".").engine.read(True, sql, ())

        for i in rs:
            self.dict_controls[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbControls['values'] = values

    def set_workstations(self):

        index = 0
        self.dict_workstations = {}
        voices = []

        sql = "SELECT workstations.workstation_id,\
                      workstations.description\
               FROM workstations\
               INNER JOIN equipments ON workstations.equipment_id = equipments.equipment_id\
               INNER JOIN sections ON workstations.section_id = sections.section_id\
               WHERE sections.section_id =?\
               AND workstations.status =1\
               ORDER BY workstations.description"

        args = (self.workstation_section_id,)

        rs = self.nametowidget(".").engine.read(True, sql, args)

        for i in rs:
            self.dict_workstations[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbWorkstations['values'] = voices

    def set_workstation(self, selected_workstation):

        try:
            key = next(key for key, value in self.dict_workstations.items()
                       if value == selected_workstation[0])
            self.cbWorkstations.current(key)
        except:
            pass

    def set_values(self,):

        try:
            key = next(key for key, value in self.dict_controls.items() if value == self.selected_batch[1])
            self.cbControls.current(key)
        except:
            pass


        try:
            key = next(key for key, value in self.dict_workstations.items() if value == self.selected_batch[3])
            self.cbWorkstations.current(key)
        except:
            pass

        self.lot_number.set(self.selected_batch[4])

        self.expiration_date.year.set(int(self.selected_batch[5][0:4]))
        self.expiration_date.month.set(int(self.selected_batch[5][5:7]))
        self.expiration_date.day.set(int(self.selected_batch[5][8:10]))

        self.target.set(round(self.selected_batch[6], 3))
        self.sd.set(round(self.selected_batch[7], 2))
        self.description.set(self.selected_batch[8])
        self.lower.set(round(self.selected_batch[9], 2))
        self.upper.set(round(self.selected_batch[10], 2))
        self.ranck.set(self.selected_batch[11])
        self.status.set(self.selected_batch[12])


    def get_values(self,):

        return [self.dict_controls[self.cbControls.current()],
                self.selected_test_method[0],
                self.dict_workstations[self.cbWorkstations.current()],
                self.lot_number.get(),
                self.expiration_date.get_date(self),
                round(self.target.get(), 3),
                round(self.sd.get(), 2),
                self.description.get(),
                round(self.lower.get(), 2),
                round(self.upper.get(), 2),
                self.ranck.get(),
                self.status.get(),
                self.nametowidget(".").engine.get_log_time(),
                self.nametowidget(".").engine.get_log_id(),
                self.nametowidget(".").engine.get_log_ip()]

    def on_set_compute(self,):

        if self.to_compute.get() == 0:
            self.txtLower.config(state=tk.DISABLED)
            self.txtUpper.config(state=tk.DISABLED)

        else:
            self.txtLower.config(state=tk.NORMAL)
            self.txtUpper.config(state=tk.NORMAL)


    def on_compute_sd(self, c, v, *args):

        try:
            if self.to_compute.get() == 1:
                upper = self.upper.get()
                lower = self.lower.get()
                try:
                    x = float(upper) - float(lower)
                    sd = round(x/3, 2)
                    self.sd.set(sd)
                except:
                    pass
        except:
            pass

    def on_check_lower_upper(self,):

        if self.to_compute.get() == 1:
            if self.lower.get() > self.upper.get():
                msg = "The lower results is major of the upper result.\nImpossible computing sd."
                messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
                return False
            else:
                return True
        else:
            return True

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return
        if self.on_check_lower_upper() == False: return
        if self.expiration_date.get_date(self) == False: return
        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql("batches", "batch_id")

                args.append(self.selected_batch[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql("batches", len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)

            self.update_batches_lists()
            self.parent.set_batches()
            self.update_remeber_batch_data()
            self.set_index(last_id)
            self.on_cancel()

    def update_remeber_batch_data(self):

        if self.set_remeber_batch_data.get():
            remember = 1
        else:
            remember = 0

        self.nametowidget(".").engine.set_remeber_batch_data(remember)

        if remember == 1:
            self.nametowidget(".").engine.batch_remembers = self.get_values()
        else:
            self.nametowidget(".").engine.batch_remembers = None
            

    def update_batches_lists(self):

        self.nametowidget(".main").set_batches()

        try:
            if self.parent.winfo_name() == "data":
                self.nametowidget(".").nametowidget("data").set_batches()
                
        except:
            self.nametowidget(".").on_log(inspect.stack()[0][3],
                                     sys.exc_info()[1],
                                     sys.exc_info()[0], sys.modules[__name__])
            
    def set_index(self, last_id):

        try:
            if self.index is not None:
                lst_index = [k for k,v in self.nametowidget(".main").dict_batchs.items() if v == self.selected_batch[0]]
            else:
                lst_index = [k for k,v in self.nametowidget(".main").dict_batchs.items() if v == last_id]

            self.parent.lstBatches.selection_set(lst_index[0])
            self.parent.lstBatches.see(lst_index[0])
            self.parent.lstBatches.event_generate("<<ListboxSelect>>")
        except:
            pass

        if self.parent.winfo_name() == "data":
            if self.index is not None:
                idx = self.index
            else:
                idx = last_id
            try:
                self.parent.lstBatches.focus()
                self.parent.lstBatches.see(idx)
                self.parent.lstBatches.selection_set(idx)
                self.parent.set_results()
                self.parent.lstBatches.event_generate("<<ListboxSelect>>")
            except:
                pass
            
    def on_cancel(self, evt=None):

        self.nametowidget(".").engine.set_instance(self, 0)

        if self.set_remeber_batch_data.get():
            remember = 1
        else:
            remember = 0

        self.nametowidget(".").engine.set_remeber_batch_data(remember)
        
        self.destroy()

