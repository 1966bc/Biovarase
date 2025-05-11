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
        super().__init__(name="control")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        self.description = tk.StringVar()
        self.reference = tk.StringVar()
        self.status = tk.BooleanVar()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.init_ui()
        self.nametowidget(".").engine.center_window_on_screen(self)


    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        ttk.Label(frm_left, text="Suppliers:").grid(row=r, sticky=tk.W)
        self.cbSuppliers = ttk.Combobox(frm_left,)
        self.cbSuppliers.grid(row=r, column=c, sticky=tk.EW, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="Description:").grid(row=r, sticky=tk.W)
        self.txDescription = ttk.Entry(frm_left, textvariable=self.description)
        self.txDescription.grid(row=r, column=c, sticky=tk.EW, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="Reference:").grid(row=r, sticky=tk.W)
        ent_reference = ttk.Entry(frm_left, textvariable=self.reference)
        ent_reference.grid(row=r, column=c, sticky=tk.EW, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        chk_status = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status,)
        chk_status.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)
        
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

    def on_open(self, ):

        self.set_suppliers()

        if self.index is not None:
            msg = "Update {0}".format(self.winfo_name().capitalize())
            self.selected_item = self.parent.selected_item
            self.set_values()
        else:
            msg = "Insert {0}".format(self.winfo_name().capitalize())
            self.status.set(1)

        self.title(msg)
        self.cbSuppliers.focus()

    def set_suppliers(self):

        index = 0
        self.dict_suppliers = {}
        values = []

        sql = "SELECT supplier_id, description\
               FROM suppliers\
               WHERE status =1\
               ORDER BY description;"
        
        rs = self.nametowidget(".").engine.read(True, sql, ())
        
        for i in rs:
            self.dict_suppliers[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbSuppliers['values'] = values


    def get_values(self,):

        return [self.dict_suppliers[self.cbSuppliers.current()],
                self.description.get(),
                self.reference.get(),
                self.status.get()]

    def set_values(self,):

        try:
            key = next(key
                       for key, value
                       in self.dict_suppliers.items()
                       if value == self.selected_item[1])
            self.cbSuppliers.current(key)
        except:
            pass

        self.description.set(self.selected_item[2])
        self.reference.set(self.selected_item[3])
        self.status.set(self.selected_item[4])

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.selected_item[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
            
            self.parent.set_values()
            self.select_item(last_id)
            self.on_cancel()

        else:
            messagebox.showinfo(self.nametowidget(".").title(),
                                self.nametowidget(".").engine.abort,
                                parent=self)

    def select_item(self, last_id=None):

        if self.index is not None:
            self.parent.lstItems.see(self.index)
            self.parent.lstItems.focus(self.index) 
            self.parent.lstItems.selection_set(self.index)
        else:
            self.parent.lstItems.see(last_id)
            self.parent.lstItems.focus(last_id) 
            self.parent.lstItems.selection_set(last_id)

    def on_cancel(self, evt=None):
        self.destroy()
