""" This is the youden module of Biovarase."""

import tkinter as tk
from tkinter import messagebox

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool


__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-12-13"
__status__ = "Production"

class UI(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='youden')

        self.parent = parent
        self.engine = kwargs['engine']
        self.minsize(1200, 600)
        self.obj = None
        self.batches = []
        self.engine.center_me(self)
        self.init_ui()


    def init_ui(self):


        f0 = self.engine.get_frame(self)

        #create graph!
        #Figure: The top level container for all the plot elements.
        #figsize:width, height in inches, figsize=(6.4, 4.8)
        self.fig = Figure()
        #fig.suptitle(self.engine.title, fontsize=20,fontweight='bold')
        #self.fig.subplots_adjust(bottom=0.10, right=0.98, left=0.10, top=0.88,wspace=0.08)
        self.fig.subplots_adjust(hspace=0.65, left=0.125, right=0.9)
        self.canvas = FigureCanvasTkAgg(self.fig, f0)
        toolbar = nav_tool(self.canvas, f0)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        f0.pack(fill=tk.BOTH, expand=1)


    def on_open(self, selected_test, batches, data):

        s = "Biovarase Youden Plot"

        title = s.format(selected_test[3])

        self.fig.suptitle(title, fontsize=14)

        s = "Youden Plot %s"%selected_test[3]

        self.um = self.get_um(selected_test[2])

        self.title(s)

        self.batches = batches

        self.set_axs(data)

        self.canvas.draw()

       
    def set_axs(self, data):

        first_sample_target =  self.batches[0][4]
        second_sample_target = self.batches[1][4]
        
        first_sample_sd = self.batches[0][5]
        second_sample_sd = self.batches[1][5]

        x = data[0]
        y = data[1]

        first_sample_low_limit = first_sample_target - (first_sample_sd*3)
        first_sample_high_limit = first_sample_target + (first_sample_sd*3)

        second_sample_low_limit = second_sample_target - (second_sample_sd*3)
        second_sample_high_limit = second_sample_target + (second_sample_sd*3)

      
        obj = self.fig.add_subplot(111, facecolor=('xkcd:light grey'),)
        obj.grid(True)

        obj.set_xlim(first_sample_low_limit, first_sample_high_limit)
            
        obj.set_ylim(second_sample_low_limit, second_sample_high_limit)

        obj.axvline(x=first_sample_target,linewidth=1, color='b')
        obj.axvline(x=first_sample_target+(first_sample_sd*2),linewidth=3, color='yellow')
        obj.axvline(x=first_sample_target-(first_sample_sd*2),linewidth=3, color='yellow')

        obj.axhline(y=second_sample_target,linewidth=1, color='b')
        obj.axhline(y=second_sample_target+(second_sample_sd*2),linewidth=3, color='yellow')
        obj.axhline(y=second_sample_target-(second_sample_sd*2),linewidth=3, color='yellow')

        obj.scatter(x, y, marker='8', s=100)


        if self.um is  not None:
            obj.set_ylabel(str(self.um[0]))
            obj.set_xlabel(str(self.um[0]))
        else:
            obj.set_ylabel("No unit assigned yet")
            obj.set_xlabel("No unit assigned yet")
            

        s = "Batch: {0} Target: {1} sd: {2} Batch: {3} Target: {4:.2f} sd: {5:.2f}"

        title = s.format(self.batches[0][2],
                         first_sample_target,
                         first_sample_sd,
                         self.batches[1][2],
                         second_sample_target,
                         second_sample_sd)

        obj.set_title(title, loc='left')

        obj.text(0.95, 0.01, 'Yellow lines rapresent 2 sd limits, blue lines rappresent selected targets',
                 verticalalignment='bottom',
                 horizontalalignment='right',
                 transform=obj.transAxes,
                 color='black',)


    def get_um(self, unit_id):

        sql = "SELECT unit FROM units WHERE unit_id =?"
        return self.engine.read(False, sql, (unit_id,))


    def on_cancel(self, evt=None):
        self.destroy()
