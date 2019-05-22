""" This is the main module of Biovarase."""
import sys
import inspect
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time


import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nav_tool
    
import matplotlib.ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib.figure import Figure
from matplotlib import gridspec

from engine import Engine



__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-05-20"
__status__ = "Production"


class Dialog(tk.Toplevel):     
    def __init__(self,parent, engine):
        super().__init__(name='tea')

        self.parent = parent
        self.minsize(1200, 600)
        self.engine = engine
        self.obj = None
        self.engine.center_me(self)
        self.init_ui()
               
          
    def init_ui(self):

       
        f0 = self.engine.get_frame(self)

        #create graph!
        #Figure: The top level container for all the plot elements.
        #figsize:width, height in inches, figsize=(6.4, 4.8)
        self.fig = Figure()
        self.fig.subplots_adjust(hspace=0.65, left=0.125, right=0.9)
        self.canvas = FigureCanvasTkAgg(self.fig, f0)
        toolbar = nav_tool(self.canvas, f0)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        f0.pack(fill=tk.BOTH, expand=1)
        

    def on_open(self,selected_test, elements):

        s = "Biovarase Total Error Plots for: {0}"

        title = s.format(selected_test[3])

        self.fig.suptitle(title, fontsize=14)

        s = "Total Error Plots %s"%selected_test[3]

        self.um = self.get_um(selected_test[2])

        self.elements = elements

        self.title(s)
        
        self.get_batches(selected_test)

        
    def get_batches(self,selected_test):

        batches = []

        sql = "SELECT *\
               FROM batches\
               WHERE test_id =? AND enable =1\
               ORDER BY expiration DESC"
        args = (selected_test[0],)
        rs = self.engine.read(True, sql, args)
        
        if rs:

            for i in rs:
                batches.append(i)
                
            self.set_values(batches)

    def set_values(self, batches):
        
        #nrows, ncols, and index
        
        count = len(batches)*100+11
        #print(count)
        sql = "SELECT * FROM lst_results WHERE batch_id = ? LIMIT ?"
       
        for batch in batches:
                            
            rs = self.engine.read(True, sql, ((batch[0],self.elements)))
            target = batch[4]
            sd = batch[5]
            args = self.engine.get_qc(target, sd, rs)

            
           
            if args is not None:

                self.set_axs(count,
                             args[0],
                             args[1],
                             args[2],
                             args[3],
                             args[4],
                             args[5],
                             args[6],
                             args[7],
                             args[10],
                             args[11],
                             batch)
                count +=1

        
        self.canvas.draw()


    def set_axs(self,count, count_rs, target, sd, series, count_series,
                compute_average, compute_sd, compute_cv, x_labels, dates, batch):

       
        #obj.clear()
        obj = self.fig.add_subplot(count, facecolor=('xkcd:light grey'),)
        obj.grid(True)

        
        et = self.engine.get_et(target, compute_average, compute_cv)
        a = self.engine.percentage(100,et)
        b = a + 4
        c = self.engine.percentage(b,target)
        #print(et,a,b,c)
        
        lines = ([],[],[],)        

        upper_limit = target + c
        lower_limit = target - c

        #print(upper_limit, target, lower_limit)

        for i in range(len(series)+1):

            lines[0].append(upper_limit)
            lines[1].append(target)
            lines[2].append(lower_limit)

        
        #it's show time
        obj.set_xticks(range(0, len(series)+1))
        #obj.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(21))
        #obj.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        obj.set_xticklabels(x_labels, rotation=70, size=6)
        obj.plot(series, marker="8", label='data')
             
        for x,y in enumerate(series):
            obj.text(x, y, str(y),)
            
        obj.plot(lines[0],color="violet",label='Tea +4',linestyle='--')
        obj.plot(lines[1],label='target', linewidth=2)
        obj.plot(lines[2],color="violet",label='Tea -4',linestyle='--')

        if self.um is  not None:
            obj.set_ylabel(str(self.um[0]))
        else:
            obj.set_ylabel("No unit assigned yet")

        s = "Batch: {0} Target: {1} SD: {2} Exp: {3} avg: {4:.2f},  std: {5:.2f} cv: {6:.2f} ET%: {7:.2f} ET+4%: {8:.2f}"

        title = s.format(batch[2],
                         batch[4],
                         batch[5],
                         batch[3],
                         compute_average, compute_sd, compute_cv, et, c)
        
        obj.set_title(title, loc='left')            

        bottom_text = ("from %s to %s"%(dates[0],dates[-1]), count_series, count_rs)

        obj.text(0.95, 0.01,
                     '%s computed %s on %s results'%bottom_text,
                     verticalalignment='bottom',
                     horizontalalignment='right',
                     transform=obj.transAxes,
                     color='black',)

 
    def get_um(self,unit_id):

        sql = "SELECT unit FROM units WHERE unit_id =?"
        return self.engine.read(False, sql, (unit_id,))

   
    def on_cancel(self, evt=None):
        self.destroy()    

