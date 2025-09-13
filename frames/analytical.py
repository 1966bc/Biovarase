# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXV (singleton + private helpers)
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk


class UI(tk.Toplevel):
    """
    Single-instance info dialog for 'Analytical Goals'.
    - __new__: reuse existing instance if still alive.
    - __init__: guarded by _is_init to avoid rebuilding UI on reuse.
    - _on_close: clears the singleton and destroys the window.
    """
    _instance = None  # class-level singleton cache

    def __new__(cls, parent):
        if cls._instance is not None:
            try:
                if cls._instance.winfo_exists():
                    return cls._instance
            except Exception:
                pass
        obj = super().__new__(cls)
        cls._instance = obj
        return obj

    def __init__(self, parent):
        # Reuse path: keep parent up to date and skip rebuild
        if getattr(self, "_is_init", False):
            self.parent = parent
            return

        super().__init__(name="analitical")

        self.parent = parent
        self.engine = self.nametowidget(".").engine

        self.attributes("-topmost", True)
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._init_ui()
        self.engine.center_window_on_screen(self)

        self._is_init = True

    def _init_ui(self):
        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        # Colors
        bg_neutral = self.engine.get_rgb(240, 240, 237)

        # Column 0: k CV
        items = (("k CV:", bg_neutral), ("0.25", "green"), ("0.50", "yellow"), ("0.75", "red"))
        r, c = 0, 0
        for text, bg in items:
            tk.Label(frm_left, bg=bg, text=text).grid(row=r, column=c, sticky=tk.W, padx=10, pady=10)
            r += 1

        # Column 1: k Bias
        items = (
            ("k Bias:", bg_neutral),
            ("0.125<= k <= 0.25", "green"),
            ("0.25<= k <= 0.375", "yellow"),
            ("k > 0.375", "red"),
        )
        r, c = 0, 1
        for text, bg in items:
            tk.Label(frm_left, bg=bg, text=text).grid(row=r, column=c, sticky=tk.W, padx=10, pady=10)
            r += 1

        # Column 2: Eta
        items = (
            ("Eta:", bg_neutral),
            ("ETa < 1.65 (0.25 CVi) + 0.125 (CVi2+ CVg2) ½ ", "green"),
            ("ETa < 1.65 (0.50 CVi) + 0.25 (CVi2 + CVg2) ½", "yellow"),
            ("ETa < 1.65 (0.75 CVi) + 0.375 (CVi2+ CVg2) ½", "red"),
        )
        r, c = 0, 2
        for text, bg in items:
            tk.Label(frm_left, bg=bg, text=text).grid(row=r, column=c, sticky=tk.W, padx=10, pady=10)
            r += 1

    def on_open(self):
        """Bring the window front and align transient to the current parent."""
        try:
            self.transient(self.parent)
        except Exception:
            pass
        self.title("Analytical Goals Explained")
        self.deiconify()
        self.lift()

    def on_cancel(self, evt=None):
        """Public alias for external callers."""
        return self._on_close(evt)

    def _on_close(self, evt=None):
        type(self)._instance = None
        super().destroy()

