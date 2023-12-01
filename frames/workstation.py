# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="workstation")
        
        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)

        self.device_id = tk.StringVar()
        self.description = tk.StringVar()
        self.serial = tk.StringVar()
        self.ranck = tk.IntVar()
        self.status = tk.BooleanVar()

        self.vcmd_int = self.nametowidget(".").engine.get_validate_integer(self)

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
        ttk.Label(frm_left, text="Equipments:").grid(row=r, sticky=tk.W)
        self.cbEquipments = ttk.Combobox(frm_left,)
        self.cbEquipments.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Device id:").grid(row=r, sticky=tk.W)
        ent_device = ttk.Entry(frm_left, textvariable=self.device_id)
        ent_device.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Description:").grid(row=r, sticky=tk.W)
        ent_description = ttk.Entry(frm_left, textvariable=self.description)
        ent_description.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Serial:").grid(row=r, sticky=tk.W)
        ent_serial = ttk.Entry(frm_left, textvariable=self.serial)
        ent_serial.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Sections:").grid(row=r, sticky=tk.W)
        self.cbSections = ttk.Combobox(frm_left,)
        self.cbSections.grid(row=r, column=c, sticky=tk.EW, **paddings)

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
        chk_status = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status,)
        chk_status.grid(row=r, column=c, sticky=tk.EW, **paddings)

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


    def on_open(self, selected_section, selected_workstation=None):

        self.selected_section = selected_section
        self.set_instruments()
        self.set_sections()
        self.set_section(selected_section)

        if self.index is not None:
            self.selected_workstation = selected_workstation
            msg = "Update {0}".format(self.winfo_name())
            self.set_values()
        else:
            msg = "Insert {0}".format(self.winfo_name())
            self.status.set(1)

        self.title(msg)
        self.cbEquipments.focus()

    def set_instruments(self):

        index = 0
        self.dict_instruments = {}
        values = []

        sql = "SELECT equipment_id, description\
               FROM equipments WHERE status =1 ORDER BY description ASC;"
        rs = self.nametowidget(".").engine.read(True, sql, ())

        for i in rs:
            self.dict_instruments[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbEquipments['values'] = values

    def set_section(self, selected_section):
        try:
            key = next(key for key, value in self.dict_sections.items() if value == selected_section[0])
            self.cbSections.current(key)
        except:
            pass
    
    def set_sections(self):

        rs_idd = self.nametowidget(".").engine.get_idd_by_section_id(self.selected_section[0])

        index = 0
        self.dict_sections = {}
        values = []

        sql = "SELECT section_id, section FROM sections WHERE lab_id =? AND status =1 ORDER BY section;"
        args = (rs_idd[3],)
        rs = self.nametowidget(".").engine.read(True, sql, args)
       
        for i in rs:
            self.dict_sections[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbSections['values'] = values


    def get_values(self,):

        return [self.dict_instruments[self.cbEquipments.current()],
                self.device_id.get(),
                self.description.get(),
                self.serial.get(),
                self.dict_sections[self.cbSections.current()],
                self.ranck.get(),
                self.status.get()]

    def set_values(self,):

        try:
            key = next(key for key, value in self.dict_instruments.items() if value == self.selected_workstation[1])
            self.cbEquipments.current(key)
        except:
            pass

        self.device_id.set(self.selected_workstation[2])
        self.description.set(self.selected_workstation[3])
        self.serial.set(self.selected_workstation[4])

        try:
            key = next(key for key, value in self.dict_sections.items() if value == self.selected_workstation[5])
            self.cbSections.current(key)
        except:
            pass

        self.ranck.set(self.selected_workstation[6])

        self.status.set(self.selected_workstation[7])

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(), self.nametowidget(".").engine.ask_to_save, parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.selected_workstation[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)

            args = (self.selected_section[0],)

            self.parent.set_workstations(args)
            

            if self.index is not None:
                try:
                    self.parent.lstWorkstations.focus(self.index)
                    self.parent.lstWorkstations.selection_set(self.index)
                except:
                    pass
            else:
                try:
                    self.parent.lstWorkstations.focus(last_id)
                    self.parent.lstWorkstations.selection_set(last_id)
                except:
                    pass
                

            self.on_cancel()

    def on_cancel(self, evt=None):
        self.destroy()
