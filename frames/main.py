# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
#-----------------------------------------------------------------------------

import sys
import inspect
import datetime
import operator
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool

import matplotlib.ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib import gridspec

import frames.license
import frames.tests
import frames.tests_methods
import frames.workstations_tests_methods
import frames.data
import frames.units
import frames.methods
import frames.specialities
import frames.equipments
import frames.workstations
import frames.controls
import frames.suppliers
import frames.wards
import frames.sections
import frames.batch
import frames.actions
import frames.notes
import frames.result
import frames.export_notes
import frames.quick_data_analysis
import frames.counts
import frames.plots
import frames.elements
import frames.zscore
import frames.set_zscore
import frames.youden
import frames.tests_sections
import frames.users
import frames.samples
import frames.analitycal_goals
import frames.tea
import frames.analytical
import frames.change_password
import frames.sites


class Main(tk.Toplevel):

    def __init__(self, parent,):
        super().__init__(name="main")

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.parent = parent
        
        self.enable_notes = tk.BooleanVar()
        self.status_bar_text = tk.StringVar()
        self.average = tk.DoubleVar()
        self.bias = tk.DoubleVar()
        self.westgard = tk.StringVar()
        self.calculated_sd = tk.DoubleVar()
        self.cva = tk.DoubleVar()
        self.range = tk.DoubleVar()
        self.elements = tk.IntVar()
        self.target = tk.DoubleVar()
        self.sd = tk.DoubleVar()
        self.zscore = tk.DoubleVar()
        self.expiration = tk.StringVar()
        self.te = tk.DoubleVar()
        self.ddof = tk.IntVar()
        self.site = tk.StringVar()

        self.selected_workstation = None

        self.init_ui()
        self.init_menu()
        self.init_status_bar()
        
        self.center_ui()

        self.nametowidget(".").engine.set_instance(self, 1)
        
    def center_ui(self):

        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        # calculate position x, y
        d = self.nametowidget(".").engine.get_dimensions()
        w = int(d['w'])
        h = int(d['h'])
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
    def init_menu(self):

        m_main = tk.Menu(self, bd=1)

        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        s_menu = tk.Menu(m_file)
        s_databases = tk.Menu(m_file)
        m_edit = tk.Menu(m_main, tearoff=0, bd=1)
        m_adm = tk.Menu(m_main, tearoff=0, bd=1)
        s_sites = tk.Menu(m_edit)
        m_batches = tk.Menu(m_main, tearoff=0, bd=1)
        m_results = tk.Menu(m_main, tearoff=0, bd=1)
        m_about = tk.Menu(m_main, tearoff=0, bd=1)

        m_main.add_cascade(label="File", underline=0, menu=m_file)
        m_main.add_cascade(label="Edit", underline=0, menu=m_edit)
        m_main.add_cascade(label="Batches", underline=0, menu=m_batches)
        m_main.add_cascade(label="Results", underline=0, menu=m_results)
        m_main.add_cascade(label="Admin", underline=0, menu=m_adm)
        m_main.add_cascade(label="?", underline=0, menu=m_about)

        items = (("Plots", self.on_plots),
                 ("Youden", self.on_youden),
                 ("Tea", self.on_tea),
                 ("Reset", self.on_reset),
                 ("Insert random results", self.on_insert_demo_result),
                 ("Analytica", self.on_analitical),
                 ("Z Score", self.on_zscore),)

        for i in items:
            m_file.add_command(label=i[0], underline=0, command=i[1])

        #keep this here
        m_file.add_cascade(label='Export', menu=s_menu, underline=0)

        items = (("Quick Data Analysis", self.on_quick_data_analysis),
                 ("Notes", self.on_export_notes),
                 ("Analytical Goals", self.on_analitycal_goals),
                 ("Counts", self.on_export_counts),
                 ("Controls List", self.on_export_controls),)

        for i in items:
            s_menu.add_command(label=i[0], underline=0, command=i[1])

        m_file.add_separator()

        m_file.add_cascade(label="Database", menu=s_databases, underline=0)
        s_databases.add_command(label="Dump",
                                underline=0,
                                command=self.on_dump)

        s_databases.add_command(label="Vacuum",
                                underline=0,
                                command=self.on_vacuum)
        
        m_file.add_command(label="Change password",
                           underline=0,
                           command=self.on_change_password)
        m_file.add_command(label="Log",
                           underline=0,
                           command=self.on_log)

        m_file.add_command(label="Exit", underline=0, command=self.on_close)

        items = (("Tests", self.on_tests),
                 ("Tests Methods", self.on_tests_methods),
                 ("Tests Sections", self.on_tests_sections),
                 ("Workstations Tests Methods", self.on_workstations_tests_methods),
                 ("Specialities", self.on_specialities),
                 ("Data", self.on_data),
                 ("Samples", self.on_samples),
                 ("Units", self.on_units),
                 ("Methods", self.on_methods),
                 ("Equipments", self.on_equipments),
                 ("Workstations", self.on_workstations),
                 ("Suppliers", self.on_suppliers),
                 ("Controls", self.on_controls),
                 ("Actions", self.on_actions),
                 ("Set Elements", self.on_elements),
                 ("Set Z Score", self.on_set_zscore),)

        for i in sorted(items, key=operator.itemgetter(0)):
            m_edit.add_command(label=i[0], underline=0, command=i[1])

        m_adm.add_command(label="Sites",
                                underline=1,
                                command=self.on_sites)

        m_adm.add_command(label="Wards",
                                underline=0,
                                command=self.on_wards)

        m_adm.add_command(label="Sections",
                                underline=1,
                                command=self.on_sections)

        m_adm.add_command(label="Users",
                                underline=0,
                                command=self.on_users)
        
        items = (("Add batch", self.on_add_batch),
                 ("Update batch", self.on_update_batch))

        for i in items:
            m_batches.add_command(label=i[0], underline=0, command=i[1])

        items = (("Add result", self.on_add_result),
                 ("Update result", self.on_update_result))

        for i in items:
            m_results.add_command(label=i[0], underline=0, command=i[1])

        m_about.add_command(label="About", underline=0, command=self.on_about)
        m_about.add_command(label="License", underline=0, command=self.on_license)
        m_about.add_command(label="Python", underline=0, command=self.on_python_version)
        m_about.add_command(label="Tkinter", underline=0, command=self.on_tkinter_version)

        for i in (m_main, m_file, ):
            i.config(bg=self.nametowidget(".").engine.get_rgb(240, 240, 237),)
            i.config(fg="black")

        self.config(menu=m_main)

    def init_ui(self):

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)

        frm_data = ttk.Frame(self.frm_main, style="App.TFrame")

        frm_lists = ttk.Frame(frm_data, style="App.TFrame")

        ttk.Label(frm_lists, text='Test Type').pack(side=tk.TOP, fill=tk.X, expand=0)

        self.cbSpecialities = ttk.Combobox(frm_lists, style="App.TCombobox")
        self.cbSpecialities = ttk.Combobox(frm_lists, state='readonly')
        self.cbSpecialities.bind("<<ComboboxSelected>>", self.on_selected_speciality)
        self.cbSpecialities.pack(side=tk.TOP, fill=tk.X, pady=5, expand=0)

        ttk.Label(frm_lists, text='Tests').pack(side=tk.TOP, fill=tk.X, expand=0)
        self.cbTests = ttk.Combobox(frm_lists, style="App.TCombobox")
        self.cbTests.bind("<<ComboboxSelected>>", self.on_selected_test)
        self.cbTests.pack(side=tk.TOP, fill=tk.X, pady=5, expand=0)

        w = ttk.LabelFrame(frm_lists, text='Workstation Data Source')
        self.lstWorkstations = self.nametowidget(".").engine.get_listbox(w, height=5, width=2, color="white")
        self.lstWorkstations.bind("<<ListboxSelect>>", self.on_selected_workstation)
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        w = ttk.LabelFrame(frm_lists, text="Batches")
        self.lstBatches = self.nametowidget(".").engine.get_listbox(w, height=5, color="white")
        self.lstBatches.selectmode = tk.MULTIPLE
        self.lstBatches.bind("<<ListboxSelect>>", self.on_selected_batch)
        self.lstBatches.bind('<Double-Button-1>', self.on_update_batch)
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        frm_stats = ttk.Frame(frm_lists, style="App.TFrame")

        w = tk.LabelFrame(frm_stats, text="Batch data", font="Helvetica 10 bold")

        ttk.Label(w, text="Target").pack()
        ttk.Label(w,
                  style="Target.TLabel",
                  anchor=tk.CENTER,
                  textvariable=self.target).pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(w, text="SD").pack()
        ttk.Label(w,
                  style="black_and_withe.TLabel",
                  anchor=tk.CENTER,
                  textvariable=self.sd).pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(w, text="TE%").pack()
        ttk.Label(w,
                  style="black_and_withe.TLabel",
                  anchor=tk.CENTER,
                  textvariable=self.te).pack(fill=tk.X, padx=2, pady=2)

        w.pack(side=tk.LEFT, fill=tk.X, expand=0)

        w = tk.LabelFrame(frm_stats, text="Cal data", font="Helvetica 10 bold")

        ttk.Label(w, text="Average").pack()
        ttk.Label(w,
                  style="Average.TLabel",
                  anchor=tk.CENTER,
                  textvariable=self.average).pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(w, text="sd").pack()
        ttk.Label(w,
                  style="black_and_withe.TLabel",
                  anchor=tk.CENTER,
                  textvariable=self.calculated_sd).pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(w, text="CV%").pack()
        ttk.Label(w,
                  style="black_and_withe.TLabel",
                  anchor=tk.CENTER,
                  textvariable=self.cva).pack(fill=tk.X, padx=2, pady=2)

        w.pack(side=tk.LEFT, fill=tk.X, expand=0)


        w = tk.LabelFrame(frm_stats, text="Other data", font="Helvetica 10 bold")

        ttk.Label(w, text="Westgard").pack()

        self.lblWestgard = ttk.Label(w,
                                     style="black_and_withe.TLabel",
                                     anchor=tk.CENTER,
                                     textvariable=self.westgard)
        self.lblWestgard.pack(fill=tk.X, padx=2, pady=2)


        ttk.Label(w, text="Range").pack()
        ttk.Label(w, style="black_and_withe.TLabel",
                  anchor=tk.CENTER,
                  textvariable=self.range).pack(fill=tk.X, padx=2, pady=2)

        ttk.Label(w, text="Bias%").pack()
        ttk.Label(w,
                  style="black_and_withe.TLabel",
                  anchor=tk.CENTER,
                  textvariable=self.bias).pack(fill=tk.X, padx=2, pady=2)

        w.pack(side=tk.RIGHT, fill=tk.X, expand=0)

        w = ttk.LabelFrame(frm_lists, text="Results")
        self.lstResults = self.nametowidget(".").engine.get_listbox(w, color="white")
        self.lstResults.bind("<<ListboxSelect>>", self.on_selected_result)
        self.lstResults.bind("<Double-Button-1>", self.on_update_result)
        w.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        #create graph!
        frm_graphs = ttk.Frame(frm_data, style="App.TFrame")
        #Figure: The top level container for all the plot elements.
        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        fig = Figure()
        #fig.suptitle(self.engine.title, fontsize=16)
        fig.subplots_adjust(bottom=0.10, right=0.96, left=0.08, top=0.95, wspace=0.10)
        self.lj = fig.add_subplot(gs[0], facecolor=("xkcd:light grey"))
        self.frq = fig.add_subplot(gs[1], facecolor=("xkcd:light grey"))
        self.canvas = FigureCanvasTkAgg(fig, frm_graphs)
        toolbar = nav_tool(self.canvas, frm_graphs)
        toolbar.update()
        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)

        frm_data.pack(fill=tk.BOTH, expand=1)
        frm_lists.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        frm_stats.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        frm_graphs.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        self.frm_main.pack(fill=tk.BOTH, expand=1)

    def init_status_bar(self):

        user = "{0} {1} on board {2}".format(self.nametowidget(".").engine.log_user[1],
                                             self.nametowidget(".").engine.log_user[2],
                                             self.nametowidget(".").engine.get_log_ip())

        msg = "Ready Player {0}".format(user)

        self.status_bar_text.set(msg)

        f = self.nametowidget(".").engine.set_font(family="TkDefaultFont", size=10, weight="bold")

        w = ttk.Frame(self.frm_main,)

        self.status = ttk.Label(w,
                                font=f,
                                textvariable=self.status_bar_text,
                                relief=tk.FLAT,
                                style="Statusbar.TLabel",
                                anchor=tk.W)

        ttk.Label(w, font=f,
                  textvariable=self.site,
                  relief=tk.FLAT,
                  anchor=tk.W).pack(side=tk.RIGHT, fill=tk.X)
        ttk.Label(w, text="Site:").pack(side=tk.RIGHT, fill=tk.X)


        ttk.Label(w, font=f,
                  textvariable=self.elements,
                  relief=tk.FLAT,
                  anchor=tk.W).pack(side=tk.RIGHT, fill=tk.X)
        ttk.Label(w, text="Elements").pack(side=tk.RIGHT, fill=tk.X)


        ttk.Label(w, font=f,
                  textvariable=self.zscore,
                  relief=tk.FLAT,
                  anchor=tk.W).pack(side=tk.RIGHT, fill=tk.X)
        ttk.Label(w, text="Z Score").pack(side=tk.RIGHT, fill=tk.X)

        ttk.Checkbutton(w,
                        text="Notes",
                        onvalue=1,
                        offvalue=0,
                        variable=self.enable_notes,).pack(side=tk.RIGHT, fill=tk.X)

        ttk.Checkbutton(w,
                        text='Delta Degree of Freedom',
                        onvalue=1,
                        offvalue=0,
                        variable=self.ddof,
                        command=self.on_ddof).pack(side=tk.RIGHT, fill=tk.X)


        self.status.pack(side=tk.LEFT, fill=tk.X, expand=1)

        w.pack(side=tk.BOTTOM, fill=tk.X)

    def on_open(self):

        site_description = self.nametowidget(".").engine.get_site_description()
        msg = "{0} {1}".format(site_description[2], site_description[4])
        self.site.set(msg)
        self.enable_notes.set(False)
        self.ddof.set(self.nametowidget(".").engine.get_ddof())
        self.elements.set(self.nametowidget(".").engine.get_elements())
        self.set_specialities()
        self.set_zscore()

    def set_elements(self):
        self.elements.set(self.nametowidget(".").engine.get_elements())

    def set_zscore(self):
        self.zscore.set(self.nametowidget(".").engine.get_zscore())

    def on_reset(self):

        self.cbSpecialities.set('')
        self.cbTests.set('')

        self.set_specialities()
        self.set_tests()
        self.set_workstations()

        self.set_elements()
        self.reset_batch_data()
        self.reset_cal_data()
        self.reset_graph()

    def reset_graph(self):

        self.lj.clear()
        self.frq.clear()
        self.lj.grid(True)
        self.frq.grid(True)
        self.canvas.draw()
        self.lstResults.delete(0, tk.END)

    def reset_batch_data(self):

        self.expiration.set('')
        self.target.set(0)
        self.sd.set(0)
        self.lstBatches.delete(0, tk.END)

    def reset_cal_data(self):

        self.average.set(0)
        self.calculated_sd.set(0)
        self.cva.set(0)
        self.bias.set(0)
        self.range.set(0)
        self.te.set(0)
        self.westgard.set('')
        self.set_westgard_alarm()

    def set_batch_data(self):

        self.expiration.set(self.selected_batch[5])
        self.target.set(round(self.selected_batch[6], 3))
        self.sd.set(round(self.selected_batch[7], 4))

    def set_calculated_data(self, mean, sd, cv, bias, crange):

        self.average.set(mean)
        self.calculated_sd.set(sd)
        self.cva.set(cv)
        self.bias.set(bias)
        self.range.set(crange)

        if self.target.get() != 0:
            et = self.nametowidget(".").engine.get_te(self.target.get(), self.average.get(), self.cva.get())
            self.te.set(et)
        else:
            self.te.set(0)

    def set_westgard(self, series):

        if len(series) > 9:
            rule = self.nametowidget(".").engine.get_westgard_violation_rule(self.selected_batch[6],
                                                           self.selected_batch[7],
                                                           series,
                                                           self.selected_batch,
                                                           self.selected_test)
        else:
            rule = "No data"

        self.westgard.set(rule)
        self.set_westgard_alarm()

    def set_westgard_alarm(self):

        if self.westgard.get() == "Accept":
            self.lblWestgard.configure(style="westgard_ok.TLabel",)
        elif self.westgard.get() in("No Data", ""):
            self.lblWestgard.configure(style="black_and_withe.TLabel",)
        else:
            self.lblWestgard.configure(style="westgard_violation.TLabel",)

    def set_specialities(self):

        self.selected_speciality = None
        index = 0
        self.dict_specialities = {}
        voices = []

        args = (self.nametowidget(".").engine.get_section_id(),)

 
        sql = "SELECT DISTINCT specialities.speciality_id,\
                               specialities.description\
               FROM sites\
               INNER JOIN wards ON sites.site_id = wards.site_id\
               INNER JOIN sections ON wards.ward_id = sections.ward_id\
               INNER JOIN tests_methods ON sections.section_id = tests_methods.section_id\
               INNER JOIN tests ON tests_methods.test_id = tests.test_id\
               INNER JOIN specialities ON tests.speciality_id = specialities.speciality_id\
               WHERE sections.section_id =?\
               AND specialities.status =1\
               ORDER BY specialities.description;"


        rs = self.nametowidget(".").engine.read(True, sql, args)

        for i in rs:
            self.dict_specialities[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbSpecialities['values'] = voices

        self.reset_batch_data()

    def set_tests(self):

        if self.cbSpecialities.current() != -1:

            self.selected_test = None
            index = 0
            self.dict_tests = {}
            voices = []

            sql = "SELECT tests_methods.test_method_id,\
                          tests.test||' '||samples.sample\
                   FROM tests\
                   INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
                   INNER JOIN samples ON tests_methods.sample_id = samples.sample_id\
                   INNER JOIN sections ON tests_methods.section_id = sections.section_id\
                   INNER JOIN wards ON sections.ward_id = wards.ward_id\
                   INNER JOIN sites ON wards.site_id = sites.site_id\
                   WHERE tests.speciality_id =?\
                   AND sections.section_id =?\
                   AND tests.status=1\
                   AND tests_methods.status=1\
                   ORDER BY tests.test;"


            args = (self.selected_speciality[0], self.nametowidget(".").engine.get_section_id())

            rs = self.nametowidget(".").engine.read(True, sql, args)

            for i in rs:
                self.dict_tests[index] = i[0]
                index += 1
                voices.append(i[1])

            self.cbTests['values'] = voices

            self.reset_batch_data()

    def set_workstations(self):

        self.lstWorkstations.delete(0, tk.END)
        self.selected_workstation = None
        index = 0
        self.dict_workstations = {}
        voices = []


        if self.cbTests.current() != -1:

            sql = "SELECT workstations.workstation_id,\
                          workstations.description,\
                          workstations.serial\
                   FROM tests_methods\
                   INNER JOIN workstations_tests_methods ON tests_methods.test_method_id = workstations_tests_methods.test_method_id\
                   INNER JOIN workstations ON workstations_tests_methods.workstation_id = workstations.workstation_id\
                   WHERE workstations_tests_methods.test_method_id =?\
                   AND workstations.status=1;"

            args = (self.selected_test_method[0], )

            rs = self.nametowidget(".").engine.read(True, sql, args)

            if rs:

                for i in rs:
                    s = "{0:15}{1:18.8}".format(i[1], i[2],)
                    self.lstWorkstations.insert(tk.END, (s))
                    self.dict_workstations[index] = i[0]
                    index += 1

                self.reset_batch_data()
                self.set_batches()
                self.lstWorkstations.select_set(0)

    def set_batches(self):

        self.lstBatches.delete(0, tk.END)

        if self.cbTests.current() != -1 and self.lstWorkstations.curselection():

            index = 0
            self.dict_batchs = {}

            sql = "SELECT batches.batch_id,\
                          batches.description,\
                          strftime('%d-%m-%Y', expiration),\
                          batches.target,\
                          batches.sd,\
                          batches.lot_number,\
                          batches.expiration\
                   FROM batches\
                   WHERE batches.test_method_id =?\
                   AND batches.workstation_id =?\
                   AND batches.status =1\
                   ORDER BY batches.ranck ASC;"

            args = (self.selected_test_method[0], self.selected_workstation[0])


            rs = self.nametowidget(".").engine.read(True, sql, args)

            if rs:

                today = datetime.date.today()

                for i in rs:

                    x = self.nametowidget(".").engine.get_expiration_date(i[2])

                    s = "{0:18} {1:10}".format(i[1], i[5])
                    
                    self.lstBatches.insert(tk.END, (s))

                    if x <= 0:
                        self.lstBatches.itemconfig(index, {"bg":"red"})
                    elif x <= 15:
                        self.lstBatches.itemconfig(index, {"bg":"yellow"})


                    self.dict_batchs[index] = i[0]
                    index += 1

                #force selection of firts item in batches listbox
                self.lstBatches.select_set(0)
                self.lstBatches.event_generate("<<ListboxSelect>>")

            else:
                self.reset_cal_data()
                self.reset_graph()

    def set_results(self,):

        try:
            self.lstResults.delete(0, tk.END)

            if self.lstWorkstations.curselection():
                index = 0
                self.dict_results = {}

                target = float(self.selected_batch[6])
                sd = float(self.selected_batch[7])

                sql = "SELECT result_id,\
                              ROUND(result,3),\
                              strftime('%d-%m-%Y', recived),\
                              status,\
                              recived\
                       FROM results\
                       WHERE batch_id =?\
                       AND workstation_id =?\
                       AND is_delete =0\
                       ORDER BY recived DESC\
                       LIMIT ?;"

                args = (self.selected_batch[0],
                        self.selected_workstation[0],
                        int(self.elements.get()))

                rs = self.nametowidget(".").engine.read(True, sql, args)
                
                if rs:

                    for i in rs:

                        s = '{0:10}{1:12}'.format(i[2], i[1])

                        self.lstResults.insert(tk.END, s)

                        result = float(round(i[1], 2))

                        is_enabled = i[3]

                        self.set_results_row_color(index, result, is_enabled, target, sd)

                        self.dict_results[index] = i[0]

                        index += 1

                    self.get_values(rs)

                else:

                    self.reset_cal_data()
                    self.reset_graph()
            else:
                self.reset_cal_data()
                self.reset_graph()

        except:
            self.nametowidget(".").engine.on_log(inspect.stack()[0][3],
                                                 sys.exc_info()[1],
                                                 sys.exc_info()[0], sys.modules[__name__])

    def on_selected_speciality(self, evt):

        if self.cbSpecialities.current() != -1:

            self.cbTests.set('')
            self.lstWorkstations.delete(0, tk.END)

            index = self.cbSpecialities.current()
            pk = self.dict_specialities[index]
            self.selected_speciality = self.nametowidget(".").engine.get_selected("specialities", "speciality_id", pk)

            self.reset_batch_data()
            self.reset_cal_data()
            self.reset_graph()

            self.set_tests()

    def on_selected_test(self, event):

        if self.cbSpecialities.current() != -1:

            if self.cbTests.current() != -1:
                
                index = self.cbTests.current()
                pk = self.dict_tests[index]

                self.selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
                self.selected_test = self.nametowidget(".").engine.get_selected("tests", "test_id", self.selected_test_method[1])

                self.reset_batch_data()
                self.reset_cal_data()
                self.reset_graph()
                
                self.set_workstations()


    def on_selected_workstation(self, evt=None):

        if self.lstWorkstations.curselection():
            
            index = self.lstWorkstations.curselection()[0]
            pk = self.dict_workstations[index]
            
            self.selected_workstation = self.nametowidget(".").engine.get_selected("workstations", "workstation_id", pk)
            
            self.reset_batch_data()
            self.reset_cal_data()
            self.reset_graph()
            self.set_batches()


    def on_selected_batch(self, evt=None):

        if self.lstBatches.curselection():
            
            index = self.lstBatches.curselection()[0]
            pk = self.dict_batchs.get(index)
            
            self.selected_batch = self.nametowidget(".").engine.get_selected("batches", "batch_id", pk)
            self.batch_index = index

            self.set_batch_data()
            self.set_results()

    def on_selected_result(self, event):

        if self.lstResults.curselection():
            
            index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(index)
            
            self.selected_result = self.nametowidget(".").engine.get_selected("results", "result_id", pk)
            
    def set_results_row_color(self, index, result, is_enabled, target, sd):

        #print(result, is_enabled, target, sd)

        if is_enabled == 0:
            self.lstResults.itemconfig(index, {"bg":"light gray"})
        else:
            d = {}
            if result >= target:
                #result > 3sd
                if result >= round((target + (sd * 3)), 2):
                    d["bg"] = "red"
                #if result is > 2sd and < +3sd
                elif result >= round((target + (sd * 2)), 2) and result <= round((target + (sd * 3)), 2):
                    d["bg"] = "yellow"

            elif result <= target:
                #result < 3sd
                if result <= round((target - (sd * 3)), 2):
                    d["bg"] = "red"
                #if result is > -2sd and < -3sd
                elif result <= round((target - (sd * 2)), 2) and result >= round((target - (sd * 3)), 2):
                    d["bg"] = "yellow"

            self.lstResults.itemconfig(index, d)

    def get_values(self, rs):

        target = self.selected_batch[6]
        sd = self.selected_batch[7]
        series = self.nametowidget(".").engine.get_series(self.selected_batch[0],
                                                          self.selected_workstation[0],
                                                          int(self.nametowidget(".").engine.get_elements()))
        mean = self.nametowidget(".").engine.get_mean(series)
        cv = self.nametowidget(".").engine.get_cv(series)
        bias = self.nametowidget(".").engine.get_bias(mean, target)
        crange = self.nametowidget(".").engine.get_range(series)
        x_labels = self.get_x_labels(rs)
        computed_sd = self.nametowidget(".").engine.get_sd(series)
        self.set_calculated_data(mean, computed_sd, cv, bias, crange)


        self.set_westgard(series)

        self.set_lj(len(rs),
                        target,
                        sd,
                        series,
                        len(series),
                        mean,
                        cv,
                        x_labels[0],
                        x_labels[1],)

        self.set_histogram(series, target, mean,)

        self.canvas.draw()


    def get_x_labels(self, rs):

        x_labels = []
        dates = []

        rs = tuple(i for i in rs if i[4] != 0)

        if rs:
            for i in reversed(rs):
                x_labels.append(i[2])
                dates.append(i[2])

        return (x_labels, dates)


    def set_lj(self, count_rs, target, sd, series, count_series,
               compute_average, compute_cv, x_labels, dates):

        self.lj.clear()
        self.lj.grid(True)
        um = self.nametowidget(".").engine.get_um(self.selected_test_method[5])
        lines = ([], [], [], [], [], [], [])

        for i in range(len(series) + 1):

            lines[0].append(target + (sd * 3))
            lines[1].append(target + (sd * 2))
            lines[2].append(target + sd)

            lines[3].append(target)

            lines[4].append(target - sd)
            lines[5].append(target - (sd * 2))
            lines[6].append(target - (sd * 3))

        #it's show time
        #self.lj.set_xticks(range(0, len(series) + 1))
        self.lj.set_xticks(range(0, len(series)))
        self.lj.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(21))
        self.lj.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        self.lj.set_xticklabels(x_labels, rotation=70, size=6)
        self.lj.plot(series, marker="8", label="data")

        for x, y in enumerate(series):
            self.lj.text(x, y, str(y),)
            
        self.lj.plot(lines[0], color="red", label="+3 sd", linestyle="--")
        self.lj.plot(lines[1], color="yellow", label="+2 sd", linestyle="--")
        self.lj.plot(lines[2], color="green", label="+1 sd", linestyle="--")
        self.lj.plot(lines[3], label="target", linewidth=2)
        self.lj.plot(lines[4], color="green", label="-1 sd", linestyle="--")
        self.lj.plot(lines[5], color="yellow", label="-2 sd", linestyle="--")
        self.lj.plot(lines[6], color="red", label="-3 sd", linestyle="--")

        if um is  not None:
            self.lj.set_ylabel(str(um[0]))
        else:
            self.lj.set_ylabel("No unit assigned yet")

        control_name = self.nametowidget(".").engine.get_control_name(self.selected_batch[1])

        s = "{0} on {1} {2} \n {3} lot {4}"

        title = s.format(self.selected_test[2],
                         self.selected_workstation[3],
                         self.selected_workstation[4],
                         control_name, self.selected_batch[4])

        self.lj.set_title(title, weight="bold", loc="center")

        bottom_text = ("from %s to %s"%(dates[0], dates[-1]), count_series, count_rs)

        self.lj.text(0.95, 0.01,
                     '%s computed %s on %s results'%bottom_text,
                     verticalalignment="bottom",
                     horizontalalignment="right",
                     transform=self.lj.transAxes,
                     color="black",
                     weight="bold")

    def set_histogram(self, series, target, avg,):
        """plot histogram of frequency distribuition"""

        self.frq.clear()
        self.frq.grid(True)

        try:
            self.frq.hist(series, density=1, color="g")
        except:
            self.frq.hist(series, normed=True, color="g")

        self.frq.axvline(target, color="orange", linewidth=2)
        self.frq.axvline(avg, color="b", linewidth=2)
        self.frq.set_ylabel('Results Frequency')
        self.frq.yaxis.set_label_position("right")

        
        um = self.nametowidget(".").engine.get_um(self.selected_test_method[5]) 
        if um is  not None:
            self.frq.set_xlabel(str(um[0]))
        else:
            self.frq.set_xlabel("No unit assigned yet")

    def on_tests(self):
        frames.tests.UI(self).on_open()

    def on_tests_methods(self):
        frames.tests_methods.UI(self).on_open()

    def on_workstations_tests_methods(self):
        frames.workstations_tests_methods.UI(self).on_open()

    def on_tests_sections(self):
        frames.tests_sections.UI(self).on_open()

    def on_specialities(self,):
        frames.specialities.UI(self).on_open()

    def on_samples(self,):
        frames.samples.UI(self).on_open()
        
    def on_units(self,):
        frames.units.UI(self).on_open()

    def on_methods(self,):
        frames.methods.UI(self).on_open()

    def on_controls(self,):
        frames.controls.UI(self).on_open()

    def on_equipments(self):
        frames.equipments.UI(self).on_open()

    def on_workstations(self,):
        frames.workstations.UI(self).on_open()

    def on_suppliers(self,):
        frames.suppliers.UI(self).on_open()

    def on_wards(self,):

        if self.nametowidget(".").engine.log_user[5] !=0:
            msg = self.nametowidget(".").engine.user_not_enable
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
        else:
            frames.wards.UI(self).on_open()

    def on_sites(self,):

        if self.nametowidget(".").engine.log_user[5] !=0:
            msg = self.nametowidget(".").engine.user_not_enable
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
        else:
            frames.sites.UI(self).on_open()        

    def on_sections(self,):

        if self.nametowidget(".").engine.log_user[5] !=0:
            msg = self.nametowidget(".").engine.user_not_enable
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
        else:
            frames.sections.UI(self).on_open()

    def on_elements(self,):
        frames.elements.UI(self).on_open()

    def on_analitical(self,):
        frames.analytical.UI(self).on_open()        

    def on_set_zscore(self,):
        frames.set_zscore.UI(self).on_open()

    def on_data(self,):
        frames.data.UI(self).on_open()

    def on_actions(self,):
        frames.actions.UI(self).on_open()

    def on_users(self,):

        if self.nametowidget(".").engine.log_user[5] !=0:
            msg = self.nametowidget(".").engine.user_not_enable
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
        else:
            frames.users.UI(self).on_open()
                    

    def on_zscore(self,):
        frames.zscore.UI(self,)

    def on_plots(self,):

        if self.cbTests.current() != -1:

            if self.lstBatches.curselection():

                index = self.cbTests.current()
                pk = self.dict_tests[index]
                selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)
                frames.plots.UI(self,).on_open(selected_test_method,
                                               self.selected_workstation,
                                               int(self.elements.get()))
            else:
                msg = "Not enough data to plot.\nSelect an instrument and a batch."
                messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
        else:
            msg = "Not enough data to plot.\nSelect a test."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

    def on_tea(self,):

        if self.cbTests.current() != -1:

            if self.lstBatches.curselection():

                index = self.cbTests.current()
                pk = self.dict_tests[index]
                selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)

                sql = "SELECT to_export FROM goals WHERE test_method_id =?;"
                args = (selected_test_method[0],)
                rs = self.nametowidget(".").engine.read(False, sql, args)
                if rs is not None:
                    if rs[0] !=0:
                        frames.tea.UI(self,).on_open(selected_test_method, self.selected_workstation, int(self.elements.get()))
                    
                else:
                    msg = "Selected test is not enable to show this plot type."
                    messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
            else:
                msg = "Not enough data to plot.\nSelect a batch."
                messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
        else:
            msg = "Not enough data to plot.\nSelect a test."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

            
    def on_youden(self,):

        if self.cbTests.current() != -1:

            if self.lstBatches.curselection():

                index = self.cbTests.current()
                pk = self.dict_tests[index]
                selected_test_method = self.nametowidget(".").engine.get_selected("tests_methods", "test_method_id", pk)

                items = self.lstBatches.curselection()

                pks = []
                batches = []

                if len(items) == 2:

                    for index in items:
                        pk = self.dict_batchs.get(index)
                        #print(pk)
                        pks.append(pk)


                    for pk in pks:
                        #print(pk)
                        batch = self.nametowidget(".").engine.get_selected("batches", "batch_id", pk)

                        batches.append(batch)

                    sql = "SELECT result_id,\
                                  ROUND(result,2),\
                                  strftime('%d-%m-%Y', recived),\
                                  status,\
                                  recived\
                           FROM results\
                           WHERE batch_id = ?\
                           AND workstation_id =?\
                           AND is_delete=0\
                           ORDER BY recived DESC\
                           LIMIT ?"

                    data = []

                    for batch in batches:
                        series = self.nametowidget(".").engine.get_series(batch[0],
                                                        self.selected_workstation[0],
                                                        int(self.nametowidget(".").engine.get_elements()))
                        data.append(series)

                    if len(data[0]) != len(data[1]):
                        msg = "Selected batches data have different size.\nIt's impossible to draw Youden plot."
                        messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

                    else:
                        frames.youden.UI(self).on_open(selected_test_method,
                                                       self.selected_workstation,
                                                       batches,
                                                       data)

                else:
                    msg = "Not data to plot a Youden chart.\nYou need to select at least two batches."
                    messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
        else:
            msg = "Not enough data to plot.\nSelect a test."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)


    def on_export_notes(self,):
        frames.export_notes.UI(self).on_open()

    def on_quick_data_analysis(self,):
        frames.quick_data_analysis.UI(self).on_open()

    def on_analitycal_goals(self,):
        frames.analitycal_goals.UI(self).on_open()        

    def on_export_counts(self,):
        frames.counts.UI(self).on_open()

    def on_export_controls(self,):

        self.nametowidget(".").engine.get_controls()

    def on_ddof(self,):

        if self.ddof.get() == True:
            self.nametowidget(".").engine.set_ddof(1)
        else:
            self.nametowidget(".").engine.set_ddof(0)

        self.ddof.set(self.nametowidget(".").engine.get_ddof())

        try:
            self.set_results()
        except AttributeError:
            msg = "Attention please.\nNo batch selected."
            messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

    def on_add_batch(self):

        if self.cbTests.current() != -1:

            if self.lstWorkstations.curselection():

                index = self.lstWorkstations.curselection()[0]
                pk = self.dict_workstations[index]
                selected_workstation = self.nametowidget(".").engine.get_selected("workstations", "workstation_id", pk)
                frames.batch.UI(self).on_open(self.selected_test_method, selected_workstation)

        else:
            msg = "Attention please.\nBefore add a batch you must select a test."
            messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

    def on_update_batch(self, evt=None):

        if self.lstBatches.curselection():
            index = self.lstBatches.curselection()[0]
            frames.batch.UI(self, index).on_open(self.selected_test_method, self.selected_workstation, self.selected_batch)
        else:
            msg = "Attention please.\nSelect a batch."
            messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

    def on_insert_demo_result(self, evt=None):

        if self.lstBatches.curselection():

            msg = "Insert 30 random results for test {0} batch {1} {2}?".format(self.selected_test[2],
                                                                                self.selected_batch[4],
                                                                                self.selected_batch[8])
            
            if messagebox.askyesno(self.nametowidget(".").title(),
                                   msg,
                                   parent=self) == True:

                sql = "DELETE FROM results WHERE batch_id =? AND workstation_id =?;"

                args = (self.selected_batch[0], self.selected_workstation[0])

                self.nametowidget(".").engine.write(sql, args)

                min_val = round((self.selected_batch[6]- self.selected_batch[7]),2)

                max_val = round((self.selected_batch[6]+ self.selected_batch[7]),2)

                sql = "INSERT INTO results(batch_id, workstation_id, result, recived, log_time) VALUES(?,?,?,?,?)"

                log_time = self.nametowidget(".").engine.get_log_time()

                for i in range(0,31):
                    
                    result = random.uniform(min_val,max_val)

                    log_time += datetime.timedelta(days=1)
                    
                    args = (self.selected_batch[0], self.selected_workstation[0], round(result,2), log_time, log_time)
                    
                    self.nametowidget(".").engine.write(sql, args)
                    
                self.set_results()

        else:
            msg = "Attention please.\nBefore add 30 random results you must select a batch."
            messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

        
    def on_add_result(self,):

        if self.lstBatches.curselection():
            frames.result.UI(self,).on_open(self.selected_test_method,
                                                     self.selected_batch,
                                                     self.selected_workstation)
        else:
            msg = "Attention please.\nBefore add a result you must select a batch."
            messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

    def on_update_result(self, evt=None):

        try:
            if self.lstResults.curselection():
                index = self.lstResults.curselection()[0]
                if self.enable_notes.get() == False:
                    frames.result.UI(self, index).on_open(self.selected_test_method,
                                                         self.selected_batch,
                                                         self.selected_workstation,
                                                         self.selected_result)

                else:
                    obj = frames.notes.UI(self)
                    obj.on_open(self.selected_test, self.selected_batch, self.selected_result)

            else:
                msg = "Attention please.\nSelect a result."
                messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

        except:
            self.nametowidget(".").engine.on_log(inspect.stack()[0][3],
                                                 sys.exc_info()[1],
                                                 sys.exc_info()[0],
                                                 sys.modules[__name__])

    def on_dump(self):
        self.nametowidget(".").engine.dump_db()
        messagebox.showinfo(self.nametowidget(".").title(), "Dump executed.", parent=self)

    def on_vacuum(self):
        sql = "VACUUM;"
        self.nametowidget(".").engine.write(sql)
        messagebox.showinfo(self.nametowidget(".").title(), "Vacuum executed.", parent=self)
        
    def on_license(self):
        frames.license.UI(self).on_open()

    def on_python_version(self):
        s = self.nametowidget(".").engine.get_python_version()
        messagebox.showinfo(self.nametowidget(".").title(), s, parent=self)

    def on_tkinter_version(self):
        s = "Tkinter patchlevel\n{0}".format(self.nametowidget(".").tk.call("info", "patchlevel"))
        messagebox.showinfo(self.nametowidget(".").title(), s, parent=self)


    def on_about(self,):
        messagebox.showinfo(self.nametowidget(".").title(),
                            self.nametowidget(".").info,
                            parent=self)

    def on_change_password(self):
        frames.change_password.UI(self, ).on_open()

    def on_log(self,):
        self.nametowidget(".").engine.get_log_file()        
        
    def on_close(self):
        self.nametowidget(".").on_exit()

