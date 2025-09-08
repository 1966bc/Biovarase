# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frames.load_tests_methods as load_tests_methods
import frames.batch as batch

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
STATUS_ACTIVE = 1


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="batches")

        # Alias to the app engine (reduces repetition and eases testing/mocking)
        self.engine = self.nametowidget(".").engine

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(400, 600)

        # Explicit state: helps IDEs and prevents "attribute appears out of nowhere"
        self.obj = None
        self.selected_workstation = None
        self.selected_test_method = None
        self.selected_batch = None
        self.tests_method_assigned = []

        self.init_ui()
        self.engine.center_window_relative_to_parent(self)
        self.engine.set_instance(self, 1)

    def init_ui(self):
        # --- Horizontal PanedWindow: 3 resizable panes (Sites | Tests | Batches)
        # Note: ttk.Panedwindow here does not support "minsize" on this Tk build,
        # so we use tk.PanedWindow instead.
        pw = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=6)
        pw.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        pane_left  = ttk.Frame(pw, style="App.TFrame")
        pane_mid   = ttk.Frame(pw, style="App.TFrame")
        pane_right = ttk.Frame(pw, style="App.TFrame")

        # Add panes with a minimum size (resizable via sash)
        pw.add(pane_left,  minsize=160)   # left pane is resizable but not too narrow
        pw.add(pane_mid,   minsize=300)
        pw.add(pane_right, minsize=300)

        # ---------- SITES (left) ----------
        cols_sites = [
            ["#0", "Sites", "w", True,  180, 220],  # stretch=True to adapt when pane resizes
            ["#1", "",      "w", True,    0,   0],
        ]
        # get_tree already packs the Treeview and the Scrollbar into the container
        self.Sites = self.engine.get_tree(pane_left, cols_sites, show="tree headings")
        # Hide all data columns (#1, #2, ...) and keep only the tree column #0 visible
        self.Sites["displaycolumns"] = ()

        self.Sites.bind("<<TreeviewSelect>>", self.on_branch_selected)
        self.Sites.bind("<Double-1>", self.on_branch_activated)

        # ---------- TESTS (center) ----------
        frm_tests = ttk.Frame(pane_mid)
        w = tk.LabelFrame(frm_tests, text='Tests')
        cols_tests = (["#0", 'dict_test_id', 'w', False, 0, 0],
                      ["#1", 'Test', 'w', True, 100, 100],
                      ["#2", 'S', 'center', True, 50, 50],
                      ["#3", 'Method', 'center', True, 50, 50],
                      ["#4", 'Unit', 'center', True, 50, 50],)
        self.lstTestsMethods = self.engine.get_tree(w, cols_tests)
        self.lstTestsMethods.bind("<<TreeviewSelect>>", self.on_test_method_selected)
        self.lstTestsMethods.bind("<Double-1>", self.on_test_method_activated)
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        frm_tests.pack(fill=tk.BOTH, expand=1)

        # ---------- BATCHES (right) ----------
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
        self.lstBatches.bind("<<TreeviewSelect>>", self.on_batch_selected)
        self.lstBatches.bind("<Double-1>", self.on_batch_activated)
        self.lblBatches.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        frm_batches.pack(fill=tk.BOTH, expand=1)

    def on_open(self,):
        msg = "{0} Management".format(self.winfo_name().title())
        self.title(msg)
        self.set_values()

    def on_reset(self):
        self.lstTestsMethods.delete(*self.lstTestsMethods.get_children())
        self.lstBatches.delete(*self.lstBatches.get_children())
        s = "{0} {1}".format("Batches", len(self.lstBatches.get_children()))
        self.lblBatches["text"] = s

    def set_values(self):
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
            section_id = self.engine.get_section_id()
            args = (section_id,)

        rs = self.engine.read(True, sql, args)

        if self.engine.log_user[5] == 0:
            for i in rs:
                # root level → parent=""
                sites = self.Sites.insert("", "end", text=i[1], values=(i[0], "sites"))

                rs_hospitals = self.load_hospitals(i[0])
                for hospital in (rs_hospitals or []):
                    hospitals = self.Sites.insert(
                        sites, "end",
                        text=hospital[1],
                        values=(hospital[0], "hospitals")
                    )

                    rs_labs = self.load_labs(hospital[0])
                    for lab in (rs_labs or []):
                        labs = self.Sites.insert(
                            hospitals, "end",
                            text=lab[1],
                            values=(lab[0], "labs")
                        )

                        rs_sections = self.load_sections(lab[0])
                        for section in (rs_sections or []):
                            sections = self.Sites.insert(
                                labs, "end",
                                text=section[1],
                                values=(section[0], "sections")
                            )

                            rs_workstations = self.load_workstations(section[0])
                            for workstation in (rs_workstations or []):
                                self.Sites.insert(
                                    sections, "end",
                                    text=workstation[1],
                                    values=(workstation[0], "workstations")
                                )
        else:
            for i in rs:
                sites = self.Sites.insert("", "end", text=i[1], values=(i[0], "sites"))

                rs_labs = self.load_labs(i[0])
                for lab in (rs_labs or []):
                    labs = self.Sites.insert(
                        sites, "end",
                        text=lab[1],
                        values=(lab[0], "labs")
                    )

                    rs_sections = self.load_sections(lab[0])
                    for section in (rs_sections or []):
                        sections = self.Sites.insert(
                            labs, "end",
                            text=section[1],
                            values=(section[0], "sections")
                        )

                        rs_workstations = self.load_workstations(section[0])
                        for workstation in (rs_workstations or []):
                            self.Sites.insert(
                                sections, "end",
                                text=workstation[1],
                                values=(workstation[0], "workstations")
                            )

    def load_hospitals(self, i):
        sql = """
            SELECT sites.site_id, suppliers.description
            FROM sites
            INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id
            WHERE sites.supplier_id = ?
              AND sites.status = 1;
        """
        return self.engine.read(True, sql, (i,))

    def load_labs(self, site_id):
        sql = """
            SELECT lab_id, lab
            FROM labs
            WHERE site_id = ?
              AND status = 1
            ORDER BY lab;
        """
        return self.engine.read(True, sql, (site_id,))

    def load_sections(self, lab_id):
        sql = """
            SELECT section_id, section
            FROM sections
            WHERE lab_id = ?
              AND status = 1
            ORDER BY section;
        """
        return self.engine.read(True, sql, (lab_id,))

    def load_workstations(self, section_id):
        sql = """
            SELECT workstation_id, description
            FROM workstations
            WHERE section_id = ?
              AND status = 1
            ORDER BY description;
        """
        return self.engine.read(True, sql, (section_id,))

    def on_branch_selected(self, evt=None):
        s = self.Sites.focus()
        if not s:
            return
        d = self.Sites.item(s)
        if d.get("values") and len(d["values"]) >= 2:
            if d["values"][1] == "workstations":
                pk = d["values"][0]
                self.selected_workstation = self.engine.get_selected("workstations", "workstation_id", pk)
                args = (self.selected_workstation[0],)
                self.set_tests_methods(args)

    def on_branch_activated(self, evt=None):
        s = self.Sites.focus()
        if not s:
            return
        d = self.Sites.item(s)
        if d.get("values") and len(d["values"]) >= 2:
            if d["values"][1] == "workstations":
                pk = d["values"][0]
                self.selected_workstation = self.engine.get_selected("workstations", "workstation_id", pk)
                self.obj = load_tests_methods.UI(self)
                self.obj.on_open(self.selected_workstation, self.tests_method_assigned)

    def set_tests_methods(self, args):
        self.tests_method_assigned = []
        self.on_reset()

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

    def set_batches(self):
        # Simple and fast cleanup
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

    def on_test_method_selected(self, evt=None):
        item_iid = self.lstTestsMethods.selection()
        if item_iid:
            pk = int(item_iid[0])
            self.selected_test_method = self.engine.get_selected("dict_tests", "dict_test_id", pk)
            self.set_batches()

    def on_test_method_activated(self, evt=None):
        if self.lstTestsMethods.focus():
            self.on_add_batch()

    def on_batch_selected(self, evt=None):
        item_iid = self.lstBatches.selection()
        if item_iid:
            pk = int(item_iid[0])
            self.selected_batch = self.engine.get_selected("batches", "batch_id", pk)

    def on_batch_activated(self, evt):
        sel_batch = self.lstBatches.selection()
        sel_test  = self.lstTestsMethods.selection()
        if not sel_batch or not sel_test:
            return
        self.obj = batch.UI(self, sel_batch)
        pk = int(sel_test[0])
        selected_test_method = self.engine.get_selected("dict_tests", "dict_test_id", pk)
        self.obj.on_open(selected_test_method, self.selected_workstation, self.selected_batch)

    def on_add_batch(self, evt=None):
        if self.lstTestsMethods.focus():
            item_iid = self.lstTestsMethods.selection()
            pk = int(item_iid[0])
            selected_test_method = self.engine.get_selected("dict_tests", "dict_test_id", pk)
            self.obj = batch.UI(self)
            self.obj.on_open(selected_test_method, self.selected_workstation,)
        else:
            msg = "Please select a test."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.engine.set_instance(self, 0)
        self.destroy()
