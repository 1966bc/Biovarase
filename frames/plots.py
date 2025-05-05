# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

try:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool

from levey_jenning_plot_helper import LeveyJenningsPlotHelper


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__()

        self.parent = parent
        self.nametowidget(".").engine.set_me_center(self)
        self.init_ui()

    def init_ui(self):
        w = ttk.Frame(self, style="App.TFrame", padding=8)
        self.fig = Figure(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, w)
        toolbar = nav_tool(self.canvas, w)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        w.pack(fill=tk.BOTH, expand=1)

    def on_open(self, selected_test_method, selected_workstation, elements):
        test_name = self.nametowidget(".").engine.get_test_name(selected_test_method[1])
        self.selected_workstation = selected_workstation
        self.selected_test_method = selected_test_method

        s = "{0} Quality Control Plots".format(test_name)
        self.um = self.nametowidget(".").engine.get_um(selected_test_method[5])
        self.elements = elements
        self.title(s)

        self.get_batches(selected_test_method)

    def get_batches(self, selected_test_method):

        batches = []
        sql = "SELECT *\
               FROM batches\
               WHERE test_method_id = ?\
               AND workstation_id =?\
               AND status =1\
               ORDER BY expiration DESC;"
        args = (selected_test_method[0], self.selected_workstation[0])
     
        rs = self.nametowidget(".").engine.read(True, sql, args)
     
        if rs:
            batches.extend(rs)  # Use extend() to add all elements
        self.set_values(batches)

    def set_figure_title(self):
        """
        Set the suptitle of the figure using selected test and workstation information.
        Call this after fig.clear()
        """
        test_name = self.nametowidget(".").engine.get_test_name(self.selected_test_method[1])
        s = "Test: {0} Workstation: {1}  Serial: {2}".format(
            test_name,
            self.selected_workstation[3],
            self.selected_workstation[4]
        )
        self.fig.suptitle(s, fontsize=14)

    def set_values(self, batches):
        
        num_rows = len(batches)
        
        self.fig.clear()

        self.set_figure_title()  

        axes = self.fig.subplots(nrows=num_rows, ncols=1, sharex=True)

        if num_rows == 1:
            axes = [axes]  

        for i, batch in enumerate(batches):
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
               LIMIT ?;"
            args = (batch[0], batch[3], self.elements)
            rs = self.nametowidget(".").engine.read(True, sql, args)
            

            if rs:
                target = batch[6]
                sd = batch[7]
                series = self.nametowidget(".").engine.get_series(
                    batch[0], self.selected_workstation[0],
                    int(self.nametowidget(".").engine.get_observations())
                )
                mean = self.nametowidget(".").engine.get_mean(series)
                cv = self.nametowidget(".").engine.get_cv(series)
                x_data = self.get_x_data(rs)

                self.set_axs(axes[i], target, sd, series, len(series),
                             mean, self.nametowidget(".").engine.get_sd(series),
                             cv, x_data['x_labels'], x_data['dates'], batch, len(rs))
            else:
                self.set_axs(axes[i], None, None, [], 0, 0, 0, 0, [], [], batch, 0)
                axes[i].text(0.5, 0.5, "No data available", ha='center', va='center', fontsize=12, color='red')


        self.fig.tight_layout()
        self.canvas.draw()

    def get_x_data(self, rs):
        x_labels = []
        dates = []
        if rs: 
            rs = tuple(i for i in rs if i[4] != 0)
            for i in reversed(rs):
                x_labels.append(i[2])
                dates.append(i[2])
        return {'x_labels': x_labels, 'dates': dates}

    def set_axs(self, ax, target, sd, series, count_series,
                compute_average, compute_sd, compute_cv, x_labels, dates, batch, count_rs):

        if series: 
            ax.grid(True)
            LeveyJenningsPlotHelper.plot_data(ax, series, x_labels)
            LeveyJenningsPlotHelper.plot_sd_lines(ax, target, sd)
            LeveyJenningsPlotHelper.format_axes(ax, x_labels, y_label="Value")

            if self.um:
                y_label = str(self.um[0])
            else:
                y_label = "No unit assigned yet"
            ax.set_ylabel(y_label)


            s = "Batch: {0} Target: {1} SD: {2} Exp: {3} avg: {4:.2f},  std: {5:.2f} cv: {6:.2f}"

            title = s.format(batch[4],
                             round(batch[6], 2),
                             round(batch[7], 3),
                             batch[5],
                             compute_average, compute_sd, compute_cv)

            ax.set_title(title, loc='left')

            bottom_text = LeveyJenningsPlotHelper.create_footer_text(dates, count_series, count_rs)
            LeveyJenningsPlotHelper.add_footer_text(ax, bottom_text)

    def on_cancel(self, evt=None):
        self.destroy()
