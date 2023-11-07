# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool

from matplotlib.figure import Figure


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__()
        
        self.parent = parent
        self.minsize(1200, 600)
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
               WHERE test_method_id = ?\
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

        #nrows, ncols, and index

        count = len(batches)*100+11
        #print(count)

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


        for batch in batches:

            args = (batch[0], self.selected_workstation[0], self.elements)

            rs = self.nametowidget(".").engine.read(True, sql, args)

            if rs:

                target = batch[6]
                sd = batch[7]
                series = self.nametowidget(".").engine.get_series(batch[0],
                                                                  self.selected_workstation[0],
                                                                  int(self.nametowidget(".").engine.get_elements()))
                mean = self.nametowidget(".").engine.get_mean(series)
                cv = self.nametowidget(".").engine.get_cv(series)
                te = self.nametowidget(".").engine.get_te(target, mean, cv)
                x_labels = self.get_x_labels(rs)

                #compute upper and lower limits
                tea = self.nametowidget(".").engine.get_tea(self.cvw, self.cvb)
                x = self.nametowidget(".").engine.percentage(tea, target)
                y = self.nametowidget(".").engine.percentage(4, x)
                #print(x,y)
                upper_limit = round(batch[9], 2)
                lower_limit = round(batch[10], 2)


                self.set_axs(count,
                             len(rs),
                             target,
                             sd,
                             series,
                             len(series),
                             mean,
                             self.nametowidget(".").engine.get_sd(series),
                             cv,
                             x_labels[0],
                             x_labels[1],
                             batch, tea,
                             upper_limit, lower_limit, te)
                count += 1


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


    def set_axs(self, count, count_rs, target, sd, series, count_series,
                compute_average, compute_sd, compute_cv, x_labels, dates, batch,
                tea, upper_limit, lower_limit, te):


        #obj.clear()
        obj = self.fig.add_subplot(count, facecolor=('xkcd:light grey'),)
        obj.grid(True)


        lines = ([], [], [],)

        for i in range(len(series)+1):

            lines[0].append(upper_limit)
            lines[1].append(target)
            lines[2].append(lower_limit)


        #it's show time
        obj.set_xticks(range(0, len(series)))
        #obj.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(21))
        #obj.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        obj.set_xticklabels(x_labels, rotation=70, size=6)
        obj.plot(series, marker="8", label='data')

        for x, y in enumerate(series):
            obj.text(x, y, str(y),)

        obj.plot(lines[0], color="violet", label='Tea +4', linestyle='--')
        obj.plot(lines[1], label='target', linewidth=2)
        obj.plot(lines[2], color="violet", label='Tea -4', linestyle='--')

        if self.um is  not None:
            obj.set_ylabel(str(self.um[0]))
        else:
            obj.set_ylabel("No unit assigned yet")

        s = "Batch: {0} Target: {1} Upper: {2} Lower: {3} ETa%: {4:.2f} Te%: {5:.2f} Z Score: {6:.2f}"

        title = s.format(batch[4],
                         round(batch[6],2),
                         upper_limit,
                         lower_limit,
                         tea,
                         te,
                         self.nametowidget(".").engine.get_zscore())

        obj.set_title(title, loc='left')

        bottom_text = ("from %s to %s"%(dates[0], dates[-1]),
                       count_series,
                       count_rs)

        obj.text(0.95, 0.01,
                 '%s computed %s on %s results'%bottom_text,
                 verticalalignment='bottom',
                 horizontalalignment='right',
                 transform=obj.transAxes,
                 color='black',)

    def on_cancel(self, evt=None):
        self.destroy()
