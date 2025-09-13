# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXV (singleton + panedwindows + private helpers)
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk


class UI(tk.Toplevel):
    """
    Single-instance window for Audit Trails.
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

        super().__init__(name="audit")

        self.parent = parent
        self.engine = self.nametowidget(".").engine

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.minsize(400, 600)

        # State
        self.obj = None
        self.selected_workstation = None
        self.selected_test_method = None
        self.selected_batch = None
        self.tests_method_assigned = []

        # UI
        self._init_ui()
        self.engine.center_window_on_screen(self)
        self.engine.set_instance(self, 1)

        self._is_init = True

    def _init_ui(self):
        # Paned layout:
        # [ PanedWindow H ]  ->  [ Sites ] | [ Tests ] | [ PanedWindow V -> Batches / Results ]
        pw_h = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=6)
        pw_h.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        pane_sites = ttk.Frame(pw_h, style="App.TFrame")
        pane_tests = ttk.Frame(pw_h, style="App.TFrame")
        pane_audits = ttk.Frame(pw_h, style="App.TFrame")

        pw_h.add(pane_sites,  minsize=180)
        pw_h.add(pane_tests,  minsize=260)
        pw_h.add(pane_audits, minsize=300)

        # ----- Sites (Tree on the left)
        frm_sections = ttk.Frame(pane_sites)
        cols_sites = (["#0", "", "w", True, 200, 220],
                      ["#1", "", "w", True,   0,   0])
        self.Sites = self.engine.get_tree(frm_sections, cols_sites, show="tree")
        self.Sites["displaycolumns"] = ()  # nasconde eventuali colonne dati
        self.Sites.pack(fill=tk.BOTH, expand=1, padx=2, pady=2)
        self.Sites.bind("<<TreeviewSelect>>", self._on_branch_selected)

        frm_sections.pack(fill=tk.BOTH, expand=1)

        # ----- Tests (center)
        frm_tests = ttk.Frame(pane_tests)
        gb_tests = tk.LabelFrame(frm_tests, text="Tests")

        cols_tests = (["#0", 'dict_test_id', 'w', False, 0, 0],
                      ["#1", 'Test',        'w', True,  0, 100],
                      ["#2", 'S',           'center', True, 0,  50],
                      ["#3", 'Method',      'center', True, 0,  50],
                      ["#4", 'Unit',        'center', True, 0,  50])
        self.lstTestsMethods = self.engine.get_tree(gb_tests, cols_tests)
        self.lstTestsMethods.bind("<<TreeviewSelect>>", self._on_test_method_selected)

        gb_tests.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        frm_tests.pack(fill=tk.BOTH, expand=1)

        # ----- Audits (right) -> Vertical PanedWindow for Batches / Results
        pw_v = tk.PanedWindow(pane_audits, orient=tk.VERTICAL, sashwidth=6)
        pw_v.pack(fill=tk.BOTH, expand=1)

        # Batches frame (top)
        frm_batches = ttk.Frame(pane_audits)
        self.lblBatches = tk.LabelFrame(frm_batches, text="Batches")

        cols_batches = (["#0", 'batch_id',    'w', False, 0,   0],
                        ["#1", 'Control',     'w', True,  0,  80],
                        ["#2", 'Lot',         'w', True,  0,  80],
                        ["#3", 'Description', 'w', True,  0,  80],
                        ["#4", 'Expiration',  'center', True, 0, 80],
                        ["#5", 'Target',      'center', True, 0, 80],
                        ["#6", 'Log time',    'center', True, 0, 100],
                        ["#7", 'Log id',      'center', True, 0, 100],
                        ["#8", 'Log ip',      'center', True, 0, 100])
        self.lstBatches = self.engine.get_tree(self.lblBatches, cols_batches)
        self.lstBatches.tag_configure('status', background=self.engine.get_rgb(211, 211, 211))
        self.lstBatches.bind("<<TreeviewSelect>>", self._on_batch_selected)

        self.lblBatches.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        frm_batches.pack(fill=tk.BOTH, expand=1)

        # Results frame (bottom)
        frm_results = ttk.Frame(pane_audits)
        self.lblResults = tk.LabelFrame(frm_results, text="Results")

        cols_results = (["#0", 'result_id', 'w', False, 0,   0],
                        ["#1", 'Run',       'w', True,  0,  80],
                        ["#2", 'Result',    'w', True,  0,  80],
                        ["#3", 'Recived',   'w', True,  0,  80],
                        ["#4", 'Log time',  'center', True, 0, 100],
                        ["#5", 'Log id',    'center', True, 0, 100],
                        ["#6", 'Log ip',    'center', True, 0, 100])
        self.lstResults = self.engine.get_tree(self.lblResults, cols_results)
        self.lstResults.tag_configure('status', background=self.engine.get_rgb(211, 211, 211))

        self.lblResults.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        frm_results.pack(fill=tk.BOTH, expand=1)

        # Add the two audit panes into the vertical PanedWindow
        pw_v.add(frm_batches, minsize=160)
        pw_v.add(frm_results, minsize=160)

    def on_open(self):
        """Title, transient follow, populate trees."""
        try:
            self.transient(self.parent)
        except Exception:
            pass
        self.title("Audit Trails")
        self._set_values()

    def on_cancel(self, evt=None):
        return self._on_close(evt)

    def _on_reset(self):
        self.lstTestsMethods.delete(*self.lstTestsMethods.get_children())
        self.lstBatches.delete(*self.lstBatches.get_children())
        self.lstResults.delete(*self.lstResults.get_children())
        self.lblBatches["text"] = "Batches 0"

    def _set_values(self):
        if self.engine.log_user[5] == 0:
            sql = (
                "SELECT sites.supplier_id, suppliers.description "
                "FROM sites "
                "INNER JOIN suppliers ON suppliers.supplier_id = sites.supplier_id "
                "WHERE sites.status = 1 "
                "GROUP BY sites.supplier_id "
                "ORDER BY suppliers.description;"
            )
            args = ()
        else:
            sql = (
                "SELECT sites.site_id, suppliers.description "
                "FROM sites "
                "INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id "
                "WHERE sites.supplier_id = ? "
                "  AND sites.status = 1 "
                "ORDER BY suppliers.description ASC;"
            )
            section_id = self.engine.get_section_id()
            related_ids = self.engine.get_related_ids_by_section(section_id)
            args = (related_ids[1],)

        rs = self.engine.read(True, sql, args)

        # Root label (optional)
        self.Sites.insert("", 0, 0, text="Sites")

        if self.engine.log_user[5] == 0:
            for sup_id, sup_desc in rs:
                sites = self.Sites.insert("", sup_id, text=sup_desc, values=(sup_id, "sites"))
                for hospital in (self._load_hospitals(sup_id) or []):
                    hospitals = self.Sites.insert(sites, hospital[0], text=hospital[1], values=(hospital[0], "hospitals"))
                    for lab in (self._load_labs(hospital[0]) or []):
                        labs = self.Sites.insert(hospitals, lab[0], text=lab[1], values=(lab[0], "labs"))
                        for section in (self._load_sections(lab[0]) or []):
                            sections = self.Sites.insert(labs, section[0], text=section[1], values=(section[0], "sections"))
                            for workstation in (self._load_workstations(section[0]) or []):
                                self.Sites.insert(sections, workstation[0], text=workstation[1], values=(workstation[0], "workstations"))
        else:
            for site_id, sup_desc in rs:
                sites = self.Sites.insert("", site_id, text=sup_desc, values=(site_id, "sites"))
                for lab in (self._load_labs(site_id) or []):
                    labs = self.Sites.insert(sites, lab[0], text=lab[1], values=(lab[0], "labs"))
                    for section in (self._load_sections(lab[0]) or []):
                        sections = self.Sites.insert(labs, section[0], text=section[1], values=(section[0], "sections"))
                        for workstation in (self._load_workstations(section[0]) or []):
                            self.Sites.insert(sections, workstation[0], text=workstation[1], values=(workstation[0], "workstations"))

    def _load_hospitals(self, supplier_id):
        sql = (
            "SELECT sites.site_id, suppliers.description "
            "FROM sites "
            "INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id "
            "WHERE sites.supplier_id = ? "
            "  AND sites.status = 1;"
        )
        return self.engine.read(True, sql, (supplier_id,))

    def _load_labs(self, site_id):
        sql = "SELECT lab_id, lab FROM labs WHERE site_id = ? AND status = 1 ORDER BY lab;"
        return self.engine.read(True, sql, (site_id,))

    def _load_sections(self, lab_id):
        sql = "SELECT section_id, section FROM sections WHERE lab_id = ? AND status = 1 ORDER BY section;"
        return self.engine.read(True, sql, (lab_id,))

    def _load_workstations(self, section_id):
        sql = "SELECT workstation_id, description FROM workstations WHERE section_id = ? AND status = 1 ORDER BY description;"
        return self.engine.read(True, sql, (section_id,))

    def _set_tests_methods(self, args):
        self.tests_method_assigned = []
        self._on_reset()

        sql = (
            "SELECT dict_tests.dict_test_id, "
            "       tests.description, "
            "       IFNULL(samples.sample,'NA')  AS samples, "
            "       IFNULL(methods.method,'NA')  AS methods, "
            "       IFNULL(units.unit,'NA')      AS units, "
            "       workstations.description, "
            "       workstations.status "
            "FROM tests "
            "INNER JOIN dict_tests       ON tests.test_id      = dict_tests.test_id "
            "INNER JOIN samples          ON dict_tests.sample_id = samples.sample_id "
            "INNER JOIN methods          ON dict_tests.method_id = methods.method_id "
            "INNER JOIN units            ON dict_tests.unit_id   = units.unit_id "
            "INNER JOIN dict_workstations ON dict_tests.dict_test_id = dict_workstations.dict_test_id "
            "INNER JOIN workstations     ON dict_workstations.workstation_id = workstations.workstation_id "
            "WHERE dict_workstations.workstation_id = ? "
            "  AND tests.status = 1 "
            "  AND dict_tests.status = 1 "
            "ORDER BY tests.description;"
        )

        rs = self.engine.read(True, sql, args)
        if rs:
            for row in rs:
                self.tests_method_assigned.append(row[0])
                tag_cfg = ("status",) if row[6] != 1 else ("",)
                self.lstTestsMethods.insert(
                    "", tk.END, iid=row[0], text=row[0],
                    values=(row[1], row[2], row[3], row[4], row[5]),
                    tags=tag_cfg
                )

    def _set_batches(self):
        self.lstBatches.delete(*self.lstBatches.get_children())
        self.lstResults.delete(*self.lstResults.get_children())

        sql = (
            "SELECT audit_batches.batch_id, "
            "       controls.description, "
            "       audit_batches.lot_number, "
            "       audit_batches.description, "
            "       strftime('%d-%m-%Y', expiration) AS expiration, "
            "       ROUND(audit_batches.target,3)    AS target, "
            "       audit_batches.log_time, "
            "       users.last_name || ' ' || users.first_name AS log_id, "
            "       audit_batches.log_ip, "
            "       audit_batches.status "
            "FROM audit_batches "
            "INNER JOIN controls ON audit_batches.control_id = controls.control_id "
            "INNER JOIN users    ON audit_batches.log_id    = users.user_id "
            "WHERE audit_batches.dict_test_id = ? "
            "  AND audit_batches.workstation_id = ? "
            "ORDER BY audit_batches.log_time;"
        )

        args = (self.selected_test_method[0], self.selected_workstation[0])
        rs = self.engine.read(True, sql, args)

        if rs:
            for row in rs:
                tag_cfg = ("status",) if row[9] != 1 else ("",)
                self.lstBatches.insert(
                    "", tk.END, text=row[0],
                    values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]),
                    tags=tag_cfg
                )

        self.lblBatches["text"] = f"Batches trails {len(self.lstBatches.get_children())}"

    def _set_results(self):
        self.lstResults.delete(*self.lstResults.get_children())

        sql = (
            "SELECT audit_results.result_id, "
            "       audit_results.run_number, "
            "       ROUND(audit_results.result,3) AS result, "
            "       strftime('%d-%m-%Y', audit_results.received) AS received, "
            "       audit_results.log_time, "
            "       users.last_name || ' ' || users.first_name AS log_id, "
            "       audit_results.log_ip, "
            "       audit_results.status "
            "FROM audit_results "
            "INNER JOIN users ON audit_results.log_id = users.user_id "
            "WHERE audit_results.batch_id = ? "
            "  AND audit_results.workstation_id = ? "
            "ORDER BY audit_results.log_time;"
        )

        args = (self.selected_batch, self.selected_workstation[0])
        rs = self.engine.read(True, sql, args)

        if rs:
            for row in rs:
                tag_cfg = ("status",) if row[7] != 1 else ("",)
                self.lstResults.insert(
                    "", tk.END, text=row[0],
                    values=(row[1], row[2], row[3], row[4], row[5], row[6]),
                    tags=tag_cfg
                )

        self.lblResults["text"] = f"Results trails {len(self.lstResults.get_children())}"

    def _on_branch_selected(self, evt=None):
        s = self.Sites.focus()
        if not s:
            return
        d = self.Sites.item(s)
        if d.get("values") and len(d["values"]) >= 2 and d["values"][1] == "workstations":
            pk = d["values"][0]
            self.selected_workstation = self.engine.get_selected("workstations", "workstation_id", pk)
            self._set_tests_methods((self.selected_workstation[0],))

    def _on_test_method_selected(self, evt=None):
        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            self.selected_test_method = self.engine.get_selected("dict_tests", "dict_test_id", pk)
            self._set_batches()

    def _on_batch_selected(self, evt=None):
        if self.lstBatches.focus():
            selected_item = self.lstBatches.focus()
            dict_item = self.lstBatches.item(selected_item)
            self.selected_batch = int(dict_item["text"])
            self._set_results()

    def _on_close(self, evt=None):
        try:
            if self.obj is not None and self.obj.winfo_exists():
                self.obj.destroy()
        except Exception:
            pass
        self.engine.set_instance(self, 0)
        type(self)._instance = None
        super().destroy()
