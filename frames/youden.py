# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
""" This is the youden module of Biovarase."""

import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool


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

        test_name  = self.nametowidget(".").engine.get_test_name(selected_test_method[1])
        
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

        first_sample_target = self.batches[0][6]
        second_sample_target = self.batches[1][6]

        first_sample_sd = self.batches[0][7]
        second_sample_sd = self.batches[1][7]

        x = data[0]
        y = data[1]

        z = list(zip(x, y))

        first_sample_low_limit = first_sample_target - (first_sample_sd*5)
        first_sample_high_limit = first_sample_target + (first_sample_sd*5)

        second_sample_low_limit = second_sample_target - (second_sample_sd*5)
        second_sample_high_limit = second_sample_target + (second_sample_sd*5)

        obj = self.fig.add_subplot(111, facecolor=('xkcd:light grey'),)

        obj.grid(True)

        obj.set_xlim(first_sample_low_limit, first_sample_high_limit)

        obj.set_ylim(second_sample_low_limit, second_sample_high_limit)

        obj.axvline(x=first_sample_target, linewidth=2, color='orange')

        obj.axvline(x=first_sample_target+(first_sample_sd), ymin=0.4, ymax=0.6, linestyle='--', color='green')
        obj.axvline(x=first_sample_target-(first_sample_sd), ymin=0.4, ymax=0.6, linestyle='--', color='green')
        obj.axvline(x=first_sample_target+(first_sample_sd*2), ymin=0.3, ymax=0.7, linestyle='--', color='yellow')
        obj.axvline(x=first_sample_target-(first_sample_sd*2), ymin=0.3, ymax=0.7, linestyle='--', color='yellow')
        obj.axvline(x=first_sample_target+(first_sample_sd*3), ymin=0.2, ymax=0.8, linestyle='--', color='red')
        obj.axvline(x=first_sample_target-(first_sample_sd*3), ymin=0.2, ymax=0.8, linestyle='--', color='red')

        obj.axhline(y=second_sample_target, linewidth=2, color='orange')
        obj.axhline(y=second_sample_target+(second_sample_sd), xmin=0.4, xmax=0.6, linestyle='--', color='green')
        obj.axhline(y=second_sample_target-(second_sample_sd), xmin=0.4, xmax=0.6, linestyle='--', color='green')
        obj.axhline(y=second_sample_target+(second_sample_sd*2), xmin=0.3, xmax=0.7, linestyle='--', color='yellow')
        obj.axhline(y=second_sample_target-(second_sample_sd*2), xmin=0.3, xmax=0.7, linestyle='--', color='yellow')
        obj.axhline(y=second_sample_target+(second_sample_sd*3), xmin=0.2, xmax=0.8, linestyle='--', color='red')
        obj.axhline(y=second_sample_target-(second_sample_sd*3), xmin=0.2, xmax=0.8, linestyle='--', color='red')

        obj.scatter(x, y, marker='8', s=80)

        for i, txt in enumerate(z):
            obj.annotate(txt, (x[i], y[i]), size=8,)


        if self.um is  not None:
            obj.set_ylabel(str(self.um[0]))
            obj.set_xlabel(str(self.um[0]))
        else:
            obj.set_ylabel("No unit assigned yet")
            obj.set_xlabel("No unit assigned yet")


        s = "Batch: {0} Target: {1:.1f} sd: {2:.1f} Batch: {3} Target: {4:.1f} sd: {5:.1f}"

        title = s.format(self.batches[0][4],
                         first_sample_target,
                         first_sample_sd,
                         self.batches[1][4],
                         second_sample_target,
                         second_sample_sd)

        obj.set_title(title, loc='left')
   
    def on_cancel(self, evt=None):
        self.destroy()
