# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXV
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    """
    Single-instance editor dialog for one 'Action' row.
    - __new__ reuses the existing instance if alive.
    - __init__ guarded by _is_init to avoid rebuilding UI on reuse.
    - _on_close() clears the singleton so the dialog can be created again.
    """
    _instance = None  # class-level singleton cache

    def __new__(cls, parent, index=None):
        if cls._instance is not None:
            try:
                if cls._instance.winfo_exists():
                    return cls._instance
            except Exception:
                pass
        obj = super().__new__(cls)
        cls._instance = obj
        return obj

    def __init__(self, parent, index=None):
        # Reuse path: keep parent/index up to date and skip rebuild
        if getattr(self, "_is_init", False):
            self.parent = parent
            self.index = index
            return

        super().__init__(name="action")  # fixed pathname: ".action"

        self.engine = self.nametowidget(".").engine
        self.parent = parent
        self.index = index  # None -> Add mode; int -> Update mode

        # Window behavior (lightweight & predictable)
        self.resizable(0, 0)
      
        # State
        self.item = tk.StringVar()
        self.status = tk.BooleanVar()

        # Close handler: free singleton
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Build UI
        self.init_ui()
        self.engine.center_window_on_screen(self)

        self._is_init = True

    def init_ui(self):
        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        # Left: fields
        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0; c = 1
        ttk.Label(frm_left, text="Action:").grid(row=r, sticky=tk.W)
        self.txtItem = ttk.Entry(frm_left, textvariable=self.item)
        self.txtItem.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status)
        chk.grid(row=r, column=c, sticky=tk.EW, **paddings)

        # Right: buttons
        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)

        r = 0; c = 0
        btn_save = ttk.Button(frm_buttons, style="App.TButton",
                              text="Save", underline=0, command=self._on_save)
        btn_save.grid(row=r, column=c, sticky=tk.EW, **paddings)
        self.bind("<Alt-s>", self._on_save)
        self.bind("<Return>", self._on_save)

        r += 1
        btn_cancel = ttk.Button(frm_buttons, style="App.TButton",
                                text="Cancel", underline=0, command=self._on_close)
        btn_cancel.grid(row=r, column=c, sticky=tk.EW, **paddings)
        self.bind("<Alt-c>", self._on_close)
        self.bind("<Escape>", self._on_close)  # togli se preferisci solo Alt+F4

    def on_open(self):
        """
        Called by parent each time the dialog is requested.
        Decides mode/title, (re)loads values, brings front, sets focus.
        """
        try:
            self.transient(self.parent)
        except Exception:
            pass
    
        if self.index is not None:
            # Update mode
            self.selected_item = self.parent.selected_item
            self._load_selected()
            title = "Update {0}".format(self.winfo_name().title())
        else:
            # Add mode
            self._clear_fields()
            title = "Add {0}".format(self.winfo_name().title())

        self.title(title)
        self.deiconify()
        self.lift()
        self.after_idle(self._focus_entry)

    def _clear_fields(self):
        self.item.set("")
        self.status.set(1)

    def _focus_entry(self):
        try:
            self.txtItem.focus_set()
            self.txtItem.selection_range(0, 'end')
        except Exception:
            pass

    def _load_selected(self):
        self.item.set(self.selected_item[1])
        self.status.set(self.selected_item[2])
        
    def _collect_values(self):
        return [self.item.get().strip(), int(self.status.get())]

    def _on_save(self, evt=None):
        if self.engine.on_fields_control(self.frm_main, self.engine.app_title) is False:
            return

        if messagebox.askyesno(self.engine.app_title, self.engine.ask_to_save, parent=self):
            args = self._collect_values()

            if self.index is not None:
                # Update
                sql = self.engine.build_sql(self.parent.table, op="update")
                args.append(self.selected_item[0])
            else:
                # Insert
                sql = self.engine.build_sql(self.parent.table, op="insert")

            last_id = self.engine.write(sql, args)

            # Refresh parent and reselect saved row
            self.parent.set_values()
            self._reselect_in_parent(last_id)

            self._on_close()
        else:
            messagebox.showinfo(self.engine.app_title, self.engine.abort, parent=self)

    def _reselect_in_parent(self, last_id=None):
        if self.index is not None:
            lst_index = [k for k, v in self.parent.dict_items.items() if v == self.selected_item[0]]
        else:
            lst_index = [k for k, v in self.parent.dict_items.items() if v == last_id]

        if lst_index:
            self.parent.lstItems.see(lst_index[0])
            self.parent.lstItems.selection_set(lst_index[0])
            self.parent.on_item_selected()

    def _on_close(self, evt=None):
        type(self)._instance = None
        super().destroy()
