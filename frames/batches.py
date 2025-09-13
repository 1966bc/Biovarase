# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV (singleton + private helpers, keep set_batches alias)
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frames.load_tests_methods as load_tests_methods
import frames.batch as batch

STATUS_ACTIVE = 1


class UI(tk.Toplevel):
    """Single-instance window to manage Batches per workstation/test."""
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
        # Guard: skip re-init when reusing the same instance
        if getattr(self, "_is_init", False):
            self.parent = parent
            return

        super().__init__(name="batches")

        # Engine alias
        self.engine = self.nametowidget(".").engine

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.minsize(400, 600)

        # Explicit state
        self.obj = None
        self.selected_workstation = None
        self.selected_test_method = None
        self.selected_batch = None
        self.tests_method_assigned = []

        self._init_ui()
        self.engine.center_window_relative_to_parent(self)
        self.engine.set_instance(self, 1)

        self._is_init = True

    def _init_ui(self):
        pw = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=6)
        pw.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        pane_left  = ttk.Frame(pw, style="App.TFrame")
        pane_mid   = ttk.Frame(pw, style="App.TFrame")
        pane_right = ttk.Frame(pw, style="App.TFrame")

        pw.add(pane_left,  minsize=160)
        pw.add(pane_mid,   minsize=300)
        pw.add(pane_right, minsize=300)

        # ----- SITES (left)
        cols_sites = [
            ["#0", "Sites", "w", True,  180, 220],
            ["#1", "",      "w", True,    0,   0],
        ]
        self.Sites = self.engine.get_tree(pane_left, cols_sites, show="tree headings")
        self.Sites["displaycolumns"] = ()
        self.Sites.bind("<<TreeviewSelect>>", self._on_branch_selected)
        self.Sites.bind("<Double-1>", self._on_branch_activated)

        # ----- TESTS (center)
        frm_tests = ttk.Frame(pane_mid)
        w = tk.LabelFrame(frm_tests, text='Tests')
        cols_tests = (["#0", 'dict_test_id', 'w', False, 0, 0],
                      ["#1", 'Test', 'w', True, 100, 100],
                      ["#2", 'S', 'center', True, 50, 50],
                      ["#3", 'Method', 'center', True, 50, 50],
                      ["#4", 'Unit', 'center', True, 50, 50],)
        self.lstTestsMethods = self.engine.get_tree(w, cols_tests)
        self.lstTestsMethods.bind("<<TreeviewSelect>>", self._on_test_method_selected)
        self.lstTestsMethods.bind("<Double-1>", self._on_test_method_activated)
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        frm_tests.pack(fill=tk.BOTH, expand=1)

        # ----- BATCHES (right)
        frm_batches = ttk.Frame(pane_right)
        self.lblBatches = tk.LabelFrame(frm_batches, text='Batches')
        cols_batches = (["#0", 'batch_id', 'w', False, 0, 0],
                        ["#1", 'Control', 'w', True, 100, 100],
                        ["#2", 'Lot', 'w', True, 80, 80],
                        ["#3", 'Description', 'w', True, 100, 100],
                        ["#4", 'Expiration', 'center', True, 80, 80],
                        ["#5", 'Target', 'center', True, 80, 80],)
        self.lstBatches = self.engine.get_tree(self.lblBatches, cols_batches)
        self.lstBatches.tag_configure('status', background=self.engine.get_rgb(211, 211, 211))
        self.lstBatches.bind("<<TreeviewSelect>>", self._on_batch_selected)
        self.lstBatches.bind("<Double-1>", self._on_batch_activated)
        self.lblBatches.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        frm_batches.pack(fill=tk.BOTH, expand=1)

    def on_open(self):
        msg = "{0} Management".format(self.winfo_name().title())
        self.title(msg)
        self._set_values()

    def on_add_batch(self, evt=None):
        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            selected_test_method = self.engine.get_selected("dict_tests", "dict_test_id", pk)
            self.obj = batch.UI(self)
            self.obj.on_open(selected_test_method, self.selected_workstation)
        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   "Please select a test.", parent=self)

    def on_cancel(self, evt=None):
        return self._on_close(evt)

    def _on_reset(self):
        self.lstTestsMethods.delete(*self.lstTestsMethods.get_children())
        self.lstBatches.delete(*self.lstBatches.get_children())
        s = "{0} {1}".format("Batches", len(self.lstBatches.get_children()))
        self.lblBatches["text"] = s

    def _set_values(self):
        if self.engine.log_user[5] == 0:
            sql = """
                SELECT sites.supplier_id, suppliers.description
                FROM sites
                INNER JOIN suppliers ON suppliers.supplier_id = sites.supplier_id
                WHERE sites.status = 1
                GROUP BY sites.supplier_id
                ORDER BY suppliers.description;
            """
            args = ()
        else:
            sql = """
                SELECT sites.site_id, suppliers.description
                FROM sites
                INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id
                INNER JOIN labs ON sites.site_id = labs.site_id
                INNER JOIN sections ON labs.lab_id = sections.lab_id
                WHERE sections.section_id = ?
                  AND sites.status = 1
                ORDER BY suppliers.description ASC;
            """
            args = (self.engine.get_section_id(),)

        rs = self.engine.read(True, sql, args)

        if self.engine.log_user[5] == 0:
            for sup_id, sup_desc in rs:
                sites = self.Sites.insert("", "end", text=sup_desc, values=(sup_id, "sites"))
                for hospital in (self._load_hospitals(sup_id) or []):
                    hospitals = self.Sites.insert(sites, "end", text=hospital[1], values=(hospital[0], "hospitals"))
                    for lab in (self._load_labs(hospital[0]) or []):
                        labs = self.Sites.insert(hospitals, "end", text=lab[1], values=(lab[0], "labs"))
                        for section in (self._load_sections(lab[0]) or []):
                            sections = self.Sites.insert(labs, "end", text=section[1], values=(section[0], "sections"))
                            for workstation in (self._load_workstations(section[0]) or []):
                                self.Sites.insert(sections, "end", text=workstation[1],
                                                  values=(workstation[0], "workstations"))
        else:
            for site_id, sup_desc in rs:
                sites = self.Sites.insert("", "end", text=sup_desc, values=(site_id, "sites"))
                for lab in (self._load_labs(site_id) or []):
                    labs = self.Sites.insert(sites, "end", text=lab[1], values=(lab[0], "labs"))
                    for section in (self._load_sections(lab[0]) or []):
                        sections = self.Sites.insert(labs, "end", text=section[1], values=(section[0], "sections"))
                        for workstation in (self._load_workstations(section[0]) or []):
                            self.Sites.insert(sections, "end", text=workstation[1],
                                              values=(workstation[0], "workstations"))

    def _load_hospitals(self, supplier_id):
        sql = """
            SELECT sites.site_id, suppliers.description
            FROM sites
            INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id
            WHERE sites.supplier_id = ?
              AND sites.status = 1;
        """
        return self.engine.read(True, sql, (supplier_id,))

    def _load_labs(self, site_id):
        sql = """
            SELECT lab_id, lab
            FROM labs
            WHERE site_id = ?
              AND status = 1
            ORDER BY lab;
        """
        return self.engine.read(True, sql, (site_id,))

    def _load_sections(self, lab_id):
        sql = """
            SELECT section_id, section
            FROM sections
            WHERE lab_id = ?
              AND status = 1
            ORDER BY section;
        """
        return self.engine.read(True, sql, (lab_id,))

    def _load_workstations(self, section_id):
        sql = """
            SELECT workstation_id, description
            FROM workstations
            WHERE section_id = ?
              AND status = 1
            ORDER BY description;
        """
        return self.engine.read(True, sql, (section_id,))

    def _set_tests_methods(self, args):
        self.tests_method_assigned = []
        self._on_reset()

        sql = """
            SELECT dict_tests.dict_test_id,
                   tests.description,
                   IFNULL(samples.sample,'NA')  AS samples,
                   IFNULL(methods.method,'NA')  AS methods,
                   IFNULL(units.unit,'NA')      AS units,
                   workstations.description,
                   workstations.status
            FROM tests
            INNER JOIN dict_tests ON tests.test_id = dict_tests.test_id
            INNER JOIN samples ON dict_tests.sample_id = samples.sample_id
            INNER JOIN methods ON dict_tests.method_id = methods.method_id
            INNER JOIN units ON dict_tests.unit_id = units.unit_id
            INNER JOIN dict_workstations ON dict_tests.dict_test_id = dict_workstations.dict_test_id
            INNER JOIN workstations ON dict_workstations.workstation_id = workstations.workstation_id
            WHERE dict_workstations.workstation_id = ?
              AND tests.status = 1
              AND dict_tests.status = 1
            ORDER BY tests.description;
        """

        rs = self.engine.read(True, sql, args)
        if rs:
            for i in rs:
                self.tests_method_assigned.append(i[0])
                tag_config = ("status",) if i[6] != STATUS_ACTIVE else ("",)
                self.lstTestsMethods.insert(
                    "", tk.END, iid=i[0], text=i[0],
                    values=(i[1], i[2], i[3], i[4], i[5]),
                    tags=tag_config
                )

    def _set_batches(self):
        self.lstBatches.delete(*self.lstBatches.get_children())

        sql = """
            SELECT batches.batch_id,
                   controls.description,
                   batches.lot_number,
                   batches.description,
                   strftime('%d-%m-%Y', expiration),
                   ROUND(batches.target, 3),
                   batches.status
            FROM batches
            INNER JOIN controls ON batches.control_id = controls.control_id
            WHERE batches.dict_test_id = ?
              AND batches.workstation_id = ?
              AND batches.lot_number IS NOT NULL
              AND batches.expiration IS NOT NULL
            ORDER BY batches.expiration DESC, batches.rank ASC;
        """

        args = (self.selected_test_method[0], self.selected_workstation[0])
        rs = self.engine.read(True, sql, args)

        if rs:
            for i in rs:
                tag_config = ("status",) if i[6] != STATUS_ACTIVE else ("",)
                self.lstBatches.insert(
                    "", tk.END, iid=i[0], text=i[0],
                    values=(i[1], i[2], i[3], i[4], i[5]),
                    tags=tag_config
                )

        s = "{0} {1}".format("Batches", len(self.lstBatches.get_children()))
        self.lblBatches["text"] = s

    # Public alias kept for compatibility (e.g., batch dialog calls this)
    def set_batches(self):
        return self._set_batches()

    # ------------------------------------------------------------- EVENTS ----
    def _on_branch_selected(self, evt=None):
        s = self.Sites.focus()
        if not s:
            return
        d = self.Sites.item(s)
        if d.get("values") and len(d["values"]) >= 2 and d["values"][1] == "workstations":
            pk = d["values"][0]
            self.selected_workstation = self.engine.get_selected("workstations", "workstation_id", pk)
            self._set_tests_methods((self.selected_workstation[0],))

    def _on_branch_activated(self, evt=None):
        s = self.Sites.focus()
        if not s:
            return
        d = self.Sites.item(s)
        if d.get("values") and len(d["values"]) >= 2 and d["values"][1] == "workstations":
            pk = d["values"][0]
            self.selected_workstation = self.engine.get_selected("workstations", "workstation_id", pk)
            self.obj = load_tests_methods.UI(self)
            self.obj.on_open(self.selected_workstation, self.tests_method_assigned)

    def _on_test_method_selected(self, evt=None):
        item_iid = self.lstTestsMethods.selection()
        if item_iid:
            pk = int(item_iid[0])
            self.selected_test_method = self.engine.get_selected("dict_tests", "dict_test_id", pk)
            self._set_batches()

    def _on_test_method_activated(self, evt=None):
        if self.lstTestsMethods.focus():
            self.on_add_batch()

    def _on_batch_selected(self, evt=None):
        item_iid = self.lstBatches.selection()
        if item_iid:
            pk = int(item_iid[0])
            self.selected_batch = self.engine.get_selected("batches", "batch_id", pk)

    def _on_batch_activated(self, evt=None):
        sel_batch = self.lstBatches.selection()
        sel_test  = self.lstTestsMethods.selection()
        if not sel_batch or not sel_test:
            return
        self.obj = batch.UI(self, sel_batch)
        pk = int(sel_test[0])
        selected_test_method = self.engine.get_selected("dict_tests", "dict_test_id", pk)
        self.obj.on_open(selected_test_method, self.selected_workstation, self.selected_batch)

    def _on_close(self, evt=None):
        try:
            if self.obj is not None and self.obj.winfo_exists():
                self.obj.destroy()
        except Exception:
            pass
        self.engine.set_instance(self, 0)
        type(self)._instance = None
        super().destroy()
