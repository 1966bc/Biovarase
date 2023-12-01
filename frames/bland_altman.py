# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
""" This is the comparisions module of Biovarase."""

import tkinter as tk
from tkinter import ttk
import numpy as np 
import matplotlib.pyplot as plt 
import scipy.stats

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="bland_altman")

        self.parent = parent
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

    def on_open(self):

        self.data = self.parent.get_experiment_data(self.parent.selected_experiment[1])
        
        s1 = self.parent.selected_experiment[9].strftime("%d-%m-%Y %H:%M:%S")
        
        s = "{0} Difference Plotter {1}".format(self.parent.test[0], s1)

        self.title(s)

        self.on_compute()

    def on_compute(self, ):

        sql = "SELECT * FROM methods_comp_results WHERE methods_comp_id=?;"

        args = (self.parent.selected_experiment[0],)
        
        rs = self.nametowidget(".").engine.read(True, sql, args)

        lst_y = []
        lst_x = []

        if rs:
            
            for i in rs:
                lst_y.append(i[2])
                lst_x.append(i[3])

            y     = np.asarray(lst_y)
            x     = np.asarray(lst_x)
            mean      = np.mean([y, x], axis=0)
            diff      = y - x                   # Difference between data1 and data2
            md        = np.mean(diff)           # Mean of the difference
            sd        = np.std(diff, axis=0)    # Standard deviation of the difference
            set_line_low    = md - 1.96*sd
            set_high_low   = md + 1.96*sd

            self.set_axs(diff, md, sd, mean, set_line_low, set_high_low)

    def get_t_student(self, differences):

        return (np.mean(differences))/(differences.std(ddof=1)/np.sqrt(len(differences)))
        
    def set_axs(self, diff, md, sd, mean, set_line_low, set_high_low):

        plt = self.fig.add_subplot(111, )

        plt.scatter(mean, diff, color = 'lightsteelblue',marker='s')
        plt.axhline(md,           color='black', linestyle='-')
        plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
        plt.axhline(md - 1.96*sd, color='gray', linestyle='--') 

        plt.set_xlabel("Means")
        plt.set_ylabel("Difference")
        plt.set_ylim(md - 3.5*sd, md + 3.5*sd)

        x_graph_pointer = np.min(mean) + (np.max(mean)-np.min(mean))*1.14

        plt.text(x_graph_pointer, md - 1.96*sd, 
            r'-1.96SD:' + "\n" + "%.2f" % set_line_low, 
            ha = "center",
            va = "center",
            )
        plt.text(x_graph_pointer, md + 1.96*sd, 
            r'+1.96SD:' + "\n" + "%.2f" % set_high_low, 
            ha = "center",
            va = "center",
            )
        plt.text(x_graph_pointer, md, 
            r'Mean:' + "\n" + "%.2f" % md, 
            ha = "center",
            va = "center",
            )

        avg = "Mean: {0}".format(round(sum(mean)/len(mean),2))
        bias = "Bias: {0}".format(round(md,2))
        standard_deviation = "Standard Deviation: {0}".format(round(sd,4))
        t_value = "t-value {0}".format(round(self.get_t_student(diff),4))

        s = "{0} {1}\n{2}\n{3}"

        title = s.format(avg,
                         bias,
                         standard_deviation,
                         t_value)

        plt.set_title(title, loc='left')
         
    def on_cancel(self, evt=None):
        self.destroy()
