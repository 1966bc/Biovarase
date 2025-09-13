#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXV (singleton + private helpers)
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    """
    Single-instance dialog for 'Analytical Goals' export.
    - __new__: reuse existing instance if alive.
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

        super().__init__(name='analytical_goals')

        self.parent = parent
        self.engine = self.nametowidget(".").engine

        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.elements = tk.IntVar()
        self.vcmd = self.engine.get_validate_integer(self)

        self._init_ui()
        self.engine.center_window_on_screen(self)

        self._is_init = True

    def _init_ui(self):
        frm_main = ttk.Frame(self, style="App.TFrame")

        frm_left = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)
        ttk.Label(frm_left, text='Set observations', style="Data.TLabel").pack()

        self.txElements = ttk.Entry(
            frm_left, width=8, justify=tk.CENTER,
            textvariable=self.elements,
            validate='key',
            validatecommand=self.vcmd
        )
        self.txElements.pack()

        frm_buttons = ttk.Frame(frm_main, style="App.TFrame", relief=tk.GROOVE, padding=8)

        bts = (("Export", 0, self._on_export, "<Alt-e>"),
               ("Cancel", 0, self._on_close,  "<Alt-c>"))

        for text, ul, cmd, accel in bts:
            ttk.Button(frm_buttons, style="App.TButton", text=text, underline=ul, command=cmd)\
               .pack(fill=tk.X, padx=5, pady=5)
            self.bind(accel, cmd)

        frm_buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        frm_main.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)

        # Keep a reference to main frame for validations
        self.frm_main = frm_main

    def on_open(self):
        """Bring to front, align transient to current parent, preload values."""
        try:
            self.transient(self.parent)
        except Exception:
            pass
        self.title("Analytical Goals")
        self.elements.set(self.engine.get_observations())
        self.deiconify()
        self.lift()
        self.after_idle(self._focus_entry)

    def on_cancel(self, evt=None):
        """Public alias for external callers."""
        return self._on_close(evt)

    def _on_export(self, evt=None):
        # Validate required field(s)
        if self.engine.on_fields_control(self.frm_main, self.engine.app_title) is False:
            return

        sql = (
            "SELECT batches.batch_id,"
            "       samples.sample,"
            "       tests.description,"
            "       batches.lot_number,"
            "       batches.expiration,"
            "       batches.target,"
            "       goals.cvw,"
            "       goals.cvb,"
            "       goals.imp,"
            "       goals.bias,"
            "       goals.teap005,"
            "       goals.teap001,"
            "       results.workstation_id "
            "FROM tests "
            "INNER JOIN dict_tests ON tests.test_id = dict_tests.test_id "
            "INNER JOIN goals ON dict_tests.dict_test_id = goals.dict_test_id "
            "INNER JOIN samples ON dict_tests.sample_id = samples.sample_id "
            "INNER JOIN batches ON dict_tests.dict_test_id = batches.dict_test_id "
            "INNER JOIN results ON batches.batch_id = results.batch_id "
            "INNER JOIN sections ON dict_tests.section_id = sections.section_id "
            "INNER JOIN labs ON sections.lab_id = labs.lab_id "
            "INNER JOIN sites ON labs.site_id = sites.site_id "
            "INNER JOIN workstations ON results.workstation_id = workstations.workstation_id "
            "WHERE tests.status = 1 "
            "  AND sections.section_id = ? "
            "  AND goals.to_export = 1 "
            "  AND batches.status = 1 "
            "  AND batches.expiration IS NOT NULL "
            "  AND results.is_delete = 0 "
            "  AND results.status = 1 "
            "GROUP BY batches.batch_id, results.workstation_id "
            "ORDER BY tests.description"
        )

        limit = int(self.elements.get())
        rs = self.engine.read(True, sql, (self.engine.get_section_id(),))

        if rs:
            self.engine.get_analitical_goals(limit, rs)
            self._on_close()
        else:
            messagebox.showwarning(self.engine.app_title, "No record data to compute.", parent=self)

    def _focus_entry(self):
        try:
            self.txElements.focus_set()
            self.txElements.selection_range(0, 'end')
        except Exception:
            pass

    def _on_close(self, evt=None):
        type(self)._instance = None
        super().destroy()
