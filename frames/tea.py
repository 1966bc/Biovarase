# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool

from total_error_plot_helper import TotalErrorPlotHelper

class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__()
        
        self.parent = parent
        #self.minsize(1200, 600)
        self.nametowidget(".").engine.center_window_relative_to_parent(self)
        self.init_ui()

    def init_ui(self):

        w = ttk.Frame(self, style="App.TFrame", padding=8)
        self.fig = Figure()
        self.fig.subplots_adjust(hspace=0.65, left=0.125, right=0.9)
        self.canvas = FigureCanvasTkAgg(self.fig, w)
        toolbar = nav_tool(self.canvas, w)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        w.pack(fill=tk.BOTH, expand=1)

    def on_open(self, selected_test_method, selected_workstation, elements):

        test_name  = self.nametowidget(".").engine.get_test_name(selected_test_method[1])

        self.cvw = selected_test_method[6]
        self.cvb = selected_test_method[7]

        self.selected_workstation = selected_workstation

        s = "Test: {0} Workstation: {1}  Serial: {2}"

        title = s.format(test_name, self.selected_workstation[3], self.selected_workstation[4])

        self.fig.suptitle(title, fontsize=14)

        s = "{0} Total Error Plots".format(test_name)

        self.um = self.nametowidget(".").engine.get_um(selected_test_method[5])

        self.elements = elements

        self.title(s)

        self.get_batches(selected_test_method)


    def get_batches(self, selected_test_method):

        batches = []

        sql = "SELECT *\
               FROM batches\
               WHERE dict_test_id = ?\
               AND workstation_id = ?\
               AND status =1\
               ORDER BY expiration DESC;"
        
        args = (selected_test_method[0], self.selected_workstation[0])
        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:

            for i in rs:
                batches.append(i)

            self.set_values(batches)

    def set_values(self, batches):
        rows = len(batches)
        cols = 1
        subplot_index = 1  # Starts from 1 as required by matplotlib subplot indexing

        sql = """
            SELECT result_id,
                   ROUND(result,2),
                   strftime('%d-%m-%Y', received),
                   status,
                   received
            FROM results
            WHERE batch_id = ?
              AND workstation_id = ?
              AND is_delete = 0
            ORDER BY received DESC
            LIMIT ?;
        """

        for batch in batches:
            args = (batch[0], self.selected_workstation[0], self.elements)
            rs = self.nametowidget(".").engine.read(True, sql, args)

            if rs:
                target = batch[6]
                sd = batch[7]
                series = self.nametowidget(".").engine.get_series(
                    batch[0],
                    self.selected_workstation[0],
                    int(self.nametowidget(".").engine.get_observations())
                )
                mean = self.nametowidget(".").engine.get_mean(series)
                cv = self.nametowidget(".").engine.get_cv(series)
                te = self.nametowidget(".").engine.get_te(target, mean, cv)
                x_data = self.get_x_data(rs)

                tea = self.nametowidget(".").engine.get_tea(self.cvw, self.cvb)
                upper_limit = round(batch[9], 2)
                lower_limit = round(batch[10], 2)
                z_score = self.nametowidget(".").engine.get_zscore()

                count = rows * 100 + cols * 10 + subplot_index  # subplot(rows, cols, i)
                self.set_axs(count,
                             len(rs),
                             target,
                             sd,
                             series,
                             len(series),
                             mean,
                             self.nametowidget(".").engine.get_sd(series),
                             cv,
                             x_data['x_labels'],
                             x_data['dates'],
                             batch,
                             tea,
                             upper_limit,
                             lower_limit,
                             te,
                             z_score)

                subplot_index += 1

        self.canvas.draw()


    def get_x_data(self, rs):
        x_labels = []
        dates = []

        rs = tuple(i for i in rs if i[4] != 0)

        if rs:
            for i in reversed(rs):
                x_labels.append(i[2])
                dates.append(i[2])

        return {'x_labels': x_labels, 'dates': dates}

    def set_axs(self, count, count_rs, target, sd, series, count_series,
                compute_average, compute_sd, compute_cv, x_labels, dates, batch,
                tea, upper_limit, lower_limit, te, z_score):  # Receive z_score

        obj = self.fig.add_subplot(count, facecolor=('xkcd:light grey'))
        obj.grid(True)

        TotalErrorPlotHelper.plot_data_and_annotations(obj, series, x_labels)
        TotalErrorPlotHelper.plot_limit_lines(obj, target, upper_limit, lower_limit, len(series))
        TotalErrorPlotHelper.set_axes_labels(obj, self.um)

        title = TotalErrorPlotHelper.create_title(batch, upper_limit, lower_limit, tea, te, z_score)  # Use helper
        obj.set_title(title, loc='left')

        bottom_text = TotalErrorPlotHelper.create_footer_text(dates, count_series, count_rs)
        TotalErrorPlotHelper.add_footer_text(obj, bottom_text)

    def on_cancel(self, evt=None):
        self.destroy()
