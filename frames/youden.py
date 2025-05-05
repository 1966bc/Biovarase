# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
# -----------------------------------------------------------------------------
"""This is the youden module of Biovarase."""

import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool

from youden_plot_helper import YoudenPlotHelper  # Import the helper class


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="youden")

        self.parent = parent
        self.batches = []
        self.nametowidget(".").engine.set_me_center(self)
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

    def on_open(self, selected_test_method, selected_workstation, batches, data):
        test_name = self.nametowidget(".").engine.get_test_name(selected_test_method[1])

        self.selected_workstation = selected_workstation

        s = "Test: {0} Workstation: {1}  Serial: {2}"
        title = s.format(test_name, self.selected_workstation[3], self.selected_workstation[4])
        self.fig.suptitle(title, fontsize=14)

        s = "{0} Youden Plot".format(test_name)

        self.um = self.nametowidget(".").engine.get_um(selected_test_method[5])

        self.title(s)

        self.batches = batches

        self.set_axs(data)

        self.canvas.draw()

    def set_axs(self, data):
        
        ax = self.fig.add_subplot(111, facecolor='xkcd:light grey')
        ax.grid(True)

        first_sample_target = self.batches[0][6]
        second_sample_target = self.batches[1][6]
        first_sample_sd = self.batches[0][7]
        second_sample_sd = self.batches[1][7]

        YoudenPlotHelper.set_axes_limits(ax, first_sample_target, first_sample_sd,
                                        second_sample_target, second_sample_sd)
        YoudenPlotHelper.plot_target_lines(ax, first_sample_target, second_sample_target)
        YoudenPlotHelper.plot_sd_lines(ax, first_sample_target, first_sample_sd,
                                      second_sample_target, second_sample_sd)
        YoudenPlotHelper.plot_data_points(ax, data[0], data[1])
        YoudenPlotHelper.set_axes_labels(ax, self.um)

        title = YoudenPlotHelper.create_title(self.batches)
        ax.set_title(title, loc='left')
        
        self.fig.tight_layout(rect=[0, 0, 1, 0.95])


    def on_cancel(self, evt=None):
        self.destroy()
