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
import frames.action as ui

SQL = "SELECT * FROM actions ORDER BY action ASC;"


class UI(tk.Toplevel):
    """
    Single-instance Toplevel for 'Actions' management.

    Singleton design:
    - __new__ returns the existing instance if the window is still alive;
      otherwise it creates a new object and stores it in the class attribute _instance.
    - __init__ is guarded by the _is_init flag to avoid re-initializing widgets
      when the same instance is reused.
    - _on_close() resets the singleton (_instance = None) so the window can be
      created again after it is closed.
    """
    _instance = None  # class-level cache for the single instance

    def __new__(cls, parent):
        """Return the existing instance if alive; otherwise create a new one."""
        if cls._instance is not None:
            try:
                if cls._instance.winfo_exists():
                    return cls._instance
            except Exception:
                # If the underlying Tk widget is in an inconsistent state,
                # ignore and recreate a fresh instance.
                pass
        obj = super().__new__(cls)
        cls._instance = obj
        return obj

    def __init__(self, parent):
        """
        Guarded initializer: when the instance is reused, skip widget rebuilds.
        """
        if getattr(self, "_is_init", False):
            # Optional: keep parent reference up to date on reuse
            self.parent = parent
            return

        super().__init__(name="actions")  # fixed pathname: ".actions"

        self.engine = self.nametowidget(".").engine
        self.parent = parent
        self.table = "actions"
        self.primary_key = "action_id"
        self.obj = None  # child dialog handle (add/update form)

        # Your UX preference: keep this window in front
        self.attributes("-topmost", True)

        # Intercept the window manager close (X / Alt+F4) to free the singleton
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.init_ui()
        self.engine.center_window_on_screen(self)

        # Mark as initialized so subsequent __init__ calls (on reuse) are no-ops
        self._is_init = True

    def init_ui(self):
        """Build the UI layout and bind basic events."""
        frm_main = ttk.Frame(self, style="App.TFrame")
        frm_left = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        sb = ttk.Scrollbar(frm_left, orient=tk.VERTICAL)
        self.lstItems = tk.Listbox(frm_left, yscrollcommand=sb.set)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        sb.config(command=self.lstItems.yview)

        self.lstItems.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=0)

        frm_buttons = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        buttons = (
            ("Add",    0, self.on_add,            "<Alt-a>"),
            ("Update", 0, self.on_item_activated, "<Alt-u>"),
            ("Cancel", 0, self.on_cancel,         "<Alt-c>"),
        )
        for text, underline, cmd, accel in buttons:
            ttk.Button(
                frm_buttons,
                style="App.TButton",
                text=text,
                underline=underline,
                command=cmd
            ).pack(fill=tk.X, padx=5, pady=5)
            self.bind(accel, cmd)

        # Common shortcuts
        self.bind("<Return>", self.on_item_activated)
        # No Escape shortcut by design (Alt+F4 is preferred)

        frm_buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)

    def on_open(self):
        """
        Called by caller code every time the window should be shown.
        Bring the window to front and refresh the list.
        No blocking waits (avoid wait_visibility race conditions).
        """
        self.title(self.winfo_name().title())
        try:
            if not self.winfo_exists():
                return
            self.deiconify()
            self.lift()
            self.set_values()
            # Set focus after idle so layout is ready; ignore if closed meanwhile.
            self.after_idle(self._focus_list)
        except Exception:
            return

    def _focus_list(self):
        """Give focus to the listbox safely (only if window still exists)."""
        if self.winfo_exists():
            try:
                self.lstItems.focus_set()
            except Exception:
                pass

    def set_values(self):
        """Reload list content from DB and apply row styles."""
        self.lstItems.delete(0, tk.END)
        index = 0
        self.dict_items = {}

        rs = self.engine.read(True, SQL, ())
        if rs:
            for row in rs:
                # row[0] = pk, row[1] = action text, row[2] = status (1/0)
                self.lstItems.insert(tk.END, f"{row[1]}")
                if row[2] != 1:
                    self.lstItems.itemconfig(index, {"bg": "light gray"})
                self.dict_items[index] = row[0]
                index += 1

    def on_add(self, evt=None):
        """Open child dialog to add a new action."""
        self.obj = ui.UI(self)
        self.obj.on_open()

    def on_item_selected(self, evt=None):
        """Track current selection and fetch full record for later operations."""
        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.engine.get_selected(self.table, self.primary_key, pk)
        else:
            self.selected_item = None

    def on_item_activated(self, evt=None):
        """Open child dialog to update the selected action."""
        if self.lstItems.curselection():
            self.on_item_selected()
            index = self.lstItems.curselection()[0]
            self.obj = ui.UI(self, index)
            self.obj.on_open()
        else:
            messagebox.showwarning(self.engine.app_title, self.engine.no_selected, parent=self)

    def on_cancel(self, evt=None):
        """Click on 'Cancel' behaves like closing the window."""
        self._on_close()

    def _on_close(self):
        """Destroy child dialog (if any), clear singleton and destroy this window."""
        try:
            if getattr(self, "obj", None) is not None and self.obj.winfo_exists():
                self.obj.destroy()
        except Exception:
            pass
        type(self)._instance = None
        super().destroy()
