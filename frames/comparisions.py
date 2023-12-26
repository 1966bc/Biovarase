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
import scipy.stats


from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="comparisions")

        self.parent = parent
        self.transient(parent)
        self.attributes('-topmost', True)
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
        
        s = "{0} Comparision Plotter {1}".format(self.parent.test[0], s1)

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
                
            y = np.array(lst_y)
            x = np.array(lst_x)
            n = np.size(x)
            x_mean = np.mean(x)
            y_mean = np.mean(y)

            slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)
            line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.4f}'
            text_slope = ("Slope: {0}".format(round(slope,4)))
            test_intercept = ("y-intercept: {0}".format(round(intercept,4)))
            y_pred = slope * x + intercept

            self.set_axs(x, y, lst_x, lst_y, line, text_slope, test_intercept, y_pred)

    def set_axs(self, x, y, lst_x, lst_y, line, text_slope, test_intercept, y_pred):

        graph = self.fig.add_subplot(111)

        graph.grid(True)
        
        graph.scatter(x, y, color = 'lightsteelblue',marker='s')
        
        graph.plot(x, y_pred, color = 'lightsteelblue',marker='s')
        
        t = "Comparative Method {0}".format(self.parent.y_comp_method[0])
        w = "Workstation {0}".format(self.parent.y_workstation_comp[0])
        m = "{0} {1}".format(t,w)
        graph.set_xlabel(m)
        
        t = "Test Method {0}".format(self.parent.x_test_method[0])
        w = "Workstation {0}".format(self.parent.x_workstation_test[0])
        m = "{0} {1}".format(t,w)                          
        graph.set_ylabel(m)


        s = "{0}\n{1}\n{2}"

        title = s.format(line,
                         text_slope,
                         test_intercept,)

        graph.set_title(title, loc='left')

        
   
    def on_cancel(self, evt=None):
        self.destroy()
