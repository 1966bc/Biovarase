# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV (singleton, private helpers, on_save -> _on_save)
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from calendarium import Calendarium


class UI(tk.Toplevel):
    """
    Single-instance editor dialog for one 'Batch' row.

    Singleton design:
    - __new__ reuses the existing instance if alive; otherwise creates a new object.
    - __init__ is guarded by _is_init to avoid rebuilding UI on reuse.
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

        super().__init__(name="batch")

        # Parent + optional selected row id (when editing)
        self.parent = parent
        self.index = index

        # Alias to the app engine
        self.engine = self.nametowidget(".").engine

        # Window behavior
        self.attributes("-topmost", True)
        self.resizable(0, 0)

        # --- Tk variables -----------------------------------------------------
        self.lot_number = tk.StringVar()
        self.description = tk.StringVar()

        # Enforce max lengths as you type (delegated to engine)
        self.lot_number.trace(
            "w",
            lambda x, y, z, c=self.engine.get_lot_length(), v=self.lot_number:
                self.engine.limit_chars(c, v, x, y, z),
        )
        self.description.trace(
            "w",
            lambda x, y, z, c=self.engine.get_batch_length(), v=self.description:
                self.engine.limit_chars(c, v, x, y, z),
        )

        self.target = tk.DoubleVar()
        self.sd = tk.DoubleVar()
        self.lower = tk.DoubleVar()
        self.upper = tk.DoubleVar()
        self.to_compute = tk.IntVar()              # 0 = Manual, 1 = Computed
        self.rank = tk.IntVar()
        self.status = tk.BooleanVar()
        self.set_remeber_batch_data = tk.BooleanVar()

        # Numeric validators provided by engine
        self.vcmd = self.engine.get_validate_float(self)
        self.vcmd_int = self.engine.get_validate_integer(self)

        # Auto-compute SD when lower/upper change (only if 'Computed' selected)
        self.lower.trace("w", lambda *args: self._on_compute_sd())
        self.upper.trace("w", lambda *args: self._on_compute_sd())

        # Basic grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        # Intercept WM close to clear singleton
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._init_ui()
        self.engine.center_window_on_screen(self)
        self.engine.set_instance(self, 1)

        # Mark as initialized so subsequent __init__ calls (on reuse) are no-ops
        self._is_init = True

    # -------------------------------------------------------------------------
    # UI construction
    # -------------------------------------------------------------------------
    def _init_ui(self):
        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_main.grid(row=0, column=0)

        # Left column with fields
        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1

        ttk.Label(frm_left, text="Control:").grid(row=r, sticky=tk.W)
        self.cbControls = ttk.Combobox(frm_left, state="readonly")
        self.cbControls.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, text="Workstations:").grid(row=r, sticky=tk.W)
        self.cbWorkstations = ttk.Combobox(frm_left, state="readonly")
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
        ttk.Label(frm_left, text="Expiration:").grid(row=r, sticky=tk.N + tk.W)
        self.expiration_date = Calendarium(self, "")
        self.expiration_date.get_calendarium(frm_left, r, c)

        r += 1
        ttk.Label(frm_left, text="Target:").grid(row=r, sticky=tk.W)
        self.txtTarget = ttk.Entry(
            frm_left,
            width=8,
            justify=tk.CENTER,
            validate="key",
            validatecommand=self.vcmd,
            textvariable=self.target,
        )
        self.txtTarget.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Lower:").grid(row=r, sticky=tk.W)
        self.txtLower = ttk.Entry(
            frm_left,
            width=8,
            justify=tk.CENTER,
            validate="key",
            validatecommand=self.vcmd,
            textvariable=self.lower,
            state=tk.DISABLED,
        )
        self.txtLower.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Upper:").grid(row=r, sticky=tk.W)
        self.txtUpper = ttk.Entry(
            frm_left,
            width=8,
            justify=tk.CENTER,
            validate="key",
            validatecommand=self.vcmd,
            textvariable=self.upper,
            state=tk.DISABLED,
        )
        self.txtUpper.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="SD:").grid(row=r, sticky=tk.W)
        self.txtSD = ttk.Entry(
            frm_left,
            width=8,
            justify=tk.CENTER,
            validate="key",
            validatecommand=self.vcmd,
            textvariable=self.sd,
        )
        self.txtSD.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, text="Rank:").grid(row=r, sticky=tk.W)
        self.txtRank = ttk.Entry(
            frm_left,
            width=8,
            justify=tk.CENTER,
            validate="key",
            validatecommand=self.vcmd_int,
            textvariable=self.rank,
        )
        self.txtRank.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(frm_left, text="Status:").grid(row=r, sticky=tk.W)
        ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.status).grid(
            row=r, column=c, sticky=tk.W
        )

        # Right column with buttons and options
        frm_buttons = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_buttons.grid(row=0, column=1, sticky=tk.NS, **paddings)

        r = 0
        c = 0
        btn = ttk.Button(
            frm_buttons, style="App.TButton", text="Save", underline=0, command=self._on_save
        )
        self.bind("<Alt-s>", self._on_save)
        self.bind("<Return>", self._on_save)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        btn = ttk.Button(
            frm_buttons, style="App.TButton", text="Cancel", underline=0, command=self._on_close
        )
        self.bind("<Alt-c>", self._on_close)
        self.bind("<Escape>", self._on_close)
        btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Checkbutton(
            frm_buttons,
            text="Remember data",
            onvalue=1,
            offvalue=0,
            variable=self.set_remeber_batch_data,
        ).grid(row=r, column=c, sticky=tk.W)

        r += 1
        frm_sd = ttk.LabelFrame(frm_buttons, style="App.TLabelframe", text="SD mode")
        frm_sd.grid(row=r, column=c, rowspan=4, sticky=tk.NW)

        voices = ["Manual", "Computed"]
        for idx, text in enumerate(voices):
            ttk.Radiobutton(
                frm_sd,
                style="App.TRadiobutton",
                text=text,
                variable=self.to_compute,
                command=self._on_set_compute,
                value=idx,
            ).grid(row=r + idx, column=c, sticky=tk.EW, **paddings)

    # -------------------------------------------------------------------------
    # Lifecycle / data population
    # -------------------------------------------------------------------------
    def on_open(self, selected_test_method, selected_workstation, selected_batch=None):
        # Ensure the dialog follows the current parent when reusing the singleton
        try:
            self.transient(self.parent)
        except Exception:
            pass

        # Needed to filter selectable workstations
        self.workstation_section_id = selected_workstation[5]

        # Carry over "remember last data" preference
        self.set_remeber_batch_data.set(self.engine.get_remeber_batch_data())

        # Fill combos and select workstation
        self._set_controls()
        self._set_workstations()
        self._set_workstation(selected_workstation)

        # Load current test & dict_test
        sql = "SELECT * FROM tests WHERE test_id = ?;"
        args = (selected_test_method[1],)
        self.selected_test = self.engine.read(False, sql, args)
        self.selected_test_method = selected_test_method

        if self.index is not None:
            # Editing an existing batch
            self.selected_batch = selected_batch
            msg = "Update {0} {1} for {2}".format(
                self.winfo_name().capitalize(), self.selected_batch[4], self.selected_test[1]
            )
            self._set_values()
            self.cbControls.focus()
        else:
            # Creating a new batch
            msg = "Insert {0} for {1}".format(self.winfo_name().capitalize(), self.selected_test[1])

            if self.set_remeber_batch_data.get() is True and self.engine.batch_remembers is not None:
                # Reapply last remembered values (defensive access to indexes)
                try:
                    key = next(
                        key for key, value in self.dict_controls.items()
                        if value == self.engine.batch_remembers[0]
                    )
                    self.cbControls.current(key)
                except Exception:
                    pass

                try:
                    self.lot_number.set(self.engine.batch_remembers[3])
                    self.description.set(self.engine.batch_remembers[7])
                    self.expiration_date.year.set(int(self.engine.batch_remembers[4].year))
                    self.expiration_date.month.set(int(self.engine.batch_remembers[4].month))
                    self.expiration_date.day.set(int(self.engine.batch_remembers[4].day))
                except Exception:
                    self.expiration_date.set_today()
            else:
                self.expiration_date.set_today()

            self.cbControls.focus()
            self.status.set(1)
            self.to_compute.set(1)  # default to 'Computed' SD
            self._on_set_compute()

        self.title(msg)

    def _set_controls(self):
        """Load active controls into the Control combobox."""
        index = 0
        self.dict_controls = {}
        values = []

        sql = "SELECT control_id, description FROM controls WHERE status = 1 ORDER BY description ASC;"
        rs = self.engine.read(True, sql, ())

        for row in rs:
            self.dict_controls[index] = row[0]
            index += 1
            values.append(row[1])

        self.cbControls["values"] = values

    def _set_workstations(self):
        """Load active workstations for the current section into the Workstations combobox."""
        index = 0
        self.dict_workstations = {}
        voices = []

        sql = (
            "SELECT workstations.workstation_id, workstations.description "
            "FROM workstations "
            "INNER JOIN equipments ON workstations.equipment_id = equipments.equipment_id "
            "INNER JOIN sections   ON workstations.section_id   = sections.section_id "
            "WHERE sections.section_id = ? "
            "AND workstations.status = 1 "
            "ORDER BY workstations.description"
        )
        args = (self.workstation_section_id,)

        rs = self.engine.read(True, sql, args)
        for row in rs:
            self.dict_workstations[index] = row[0]
            index += 1
            voices.append(row[1])

        self.cbWorkstations["values"] = voices

    def _set_workstation(self, selected_workstation):
        """Select the workstation in the combobox based on the passed record."""
        try:
            key = next(
                key for key, value in self.dict_workstations.items()
                if value == selected_workstation[0]
            )
            self.cbWorkstations.current(key)
        except Exception:
            pass

    def _set_values(self):
        """Populate widgets with the currently selected batch values (edit mode)."""
        # Control
        try:
            key = next(
                key for key, value in self.dict_controls.items()
                if value == self.selected_batch[1]
            )
            self.cbControls.current(key)
        except Exception:
            pass

        # Workstation
        try:
            key = next(
                key for key, value in self.dict_workstations.items()
                if value == self.selected_batch[3]
            )
            self.cbWorkstations.current(key)
        except Exception:
            pass

        self.lot_number.set(self.selected_batch[4])

        # Expiration (YYYY-MM-DD)
        try:
            self.expiration_date.year.set(int(self.selected_batch[5][0:4]))
            self.expiration_date.month.set(int(self.selected_batch[5][5:7]))
            self.expiration_date.day.set(int(self.selected_batch[5][8:10]))
        except Exception:
            # Fallback: today, if parsing fails
            self.expiration_date.set_today()

        # Numerics
        self.target.set(round(self.selected_batch[6], 3))
        self.sd.set(round(self.selected_batch[7], 2))
        self.description.set(self.selected_batch[8])
        self.lower.set(round(self.selected_batch[9], 2))
        self.upper.set(round(self.selected_batch[10], 2))
        self.rank.set(self.selected_batch[11])
        self.status.set(self.selected_batch[12])

    # -------------------------------------------------------------------------
    # Helpers / validation
    # -------------------------------------------------------------------------
    def _get_values(self):
        """Collect values for INSERT/UPDATE. Keep order consistent with table schema."""
        return [
            self.dict_controls.get(self.cbControls.current()),          # control_id
            self.selected_test_method[0],                               # dict_test_id
            self.dict_workstations.get(self.cbWorkstations.current()),  # workstation_id
            self.lot_number.get(),
            self.expiration_date.get_date(self),
            round(self.target.get(), 3),
            round(self.sd.get(), 2),
            self.description.get(),
            round(self.lower.get(), 2),
            round(self.upper.get(), 2),
            self.rank.get(),
            self.status.get(),
            self.engine.get_log_time(),
            self.engine.get_log_id(),
            self.engine.get_log_ip(),
        ]

    def _on_set_compute(self):
        """Enable/disable Lower/Upper fields based on SD mode."""
        if self.to_compute.get() == 0:
            self.txtLower.config(state=tk.DISABLED)
            self.txtUpper.config(state=tk.DISABLED)
        else:
            self.txtLower.config(state=tk.NORMAL)
            self.txtUpper.config(state=tk.NORMAL)
        self._on_compute_sd()  # refresh SD

    def _on_compute_sd(self):
        """Recompute SD when in 'Computed' mode: SD = (Upper - Lower) / 3 (rounded to 2)."""
        if self.to_compute.get() != 1:
            return
        try:
            upper = float(self.upper.get())
            lower = float(self.lower.get())
            if upper >= lower:
                self.sd.set(round((upper - lower) / 3.0, 2))
        except Exception:
            # Ignore partial/invalid inputs while typing
            pass

    def _check_lower_upper(self):
        """Basic semantic check: Lower must not exceed Upper when computing SD."""
        if self.to_compute.get() == 1 and self.lower.get() > self.upper.get():
            msg = "The lower result is greater than the upper result.\nImpossible to compute SD."
            messagebox.showwarning(self.engine.app_title, msg, parent=self)
            return False
        return True

    # -------------------------------------------------------------------------
    # Persistence
    # -------------------------------------------------------------------------
    def _on_save(self, evt=None):
        # Validate required fields in the form
        if self.engine.on_fields_control(self.frm_main, self.engine.app_title) is False:
            return
        if self._check_lower_upper() is False:
            return
        if self.expiration_date.get_date(self) is False:
            return

        if messagebox.askyesno(self.engine.app_title, self.engine.ask_to_save, parent=self) is True:
            args = self._get_values()

            if self.index is not None:
                # UPDATE
                sql = self.engine.build_sql("batches", op="update")
                args.append(self.selected_batch[0])
            else:
                # INSERT
                sql = self.engine.build_sql("batches", op="insert")

            last_id = self.engine.write(sql, args)

            # Refresh both the child and main views
            self.parent.set_batches()
            self.nametowidget(".main").set_batches()

            # Persist "remember" preference (+ optionally the last data)
            self._update_remeber_batch_data()

            # Restore selection on the saved item
            self._set_index(last_id)

            # Close dialog
            self._on_close()

    def _update_remeber_batch_data(self):
        """Store the 'remember' flag and optionally the last entered values in the engine."""
        remember = 1 if self.set_remeber_batch_data.get() else 0
        self.engine.set_remeber_batch_data(remember)
        if remember == 1:
            self.engine.batch_remembers = self._get_values()
        else:
            self.engine.batch_remembers = None

    def _set_index(self, last_id):
        """
        Select the saved/updated row in both the child and main Listboxes.
        Works by finding the index whose pk matches the saved batch_id.
        """
        # Determine target DB id
        target_id = self.selected_batch[0] if self.index is not None else last_id

        # Child list (Batches window)
        try:
            if getattr(self.parent, "dict_batchs", None):
                # find listbox index by batch_id
                idxs = [i for i, bid in self.parent.dict_batchs.items() if bid == target_id]
                if idxs:
                    i = idxs[0]
                    self.parent.lstBatches.focus()
                    self.parent.lstBatches.see(i)
                    self.parent.lstBatches.selection_set(i)
                    self.parent.lstBatches.event_generate("<<ListboxSelect>>")
        except Exception:
            pass

        # Main window listbox
        try:
            main_window = self.nametowidget(".main")
            if getattr(main_window, "dict_batchs", None):
                idxs = [i for i, bid in main_window.dict_batchs.items() if bid == target_id]
                if idxs:
                    i = idxs[0]
                    main_window.lstBatches.selection_set(i)
                    main_window.lstBatches.see(i)
                    main_window.lstBatches.event_generate("<<ListboxSelect>>")
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Closing
    # -------------------------------------------------------------------------
    def on_cancel(self, evt=None):
        """Public alias kept for external callers; forwards to _on_close()."""
        return self._on_close(evt)

    def _on_close(self, evt=None):
        """Single source of truth for closing: clear singleton and destroy."""
        try:
            self.engine.set_instance(self, 0)
        except Exception:
            pass
        type(self)._instance = None
        super().destroy()
