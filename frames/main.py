""" This is the main module of Biovarase."""
import sys
import inspect
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


import matplotlib.pyplot as plt

plt.rcParams.update({'figure.max_open_warning': 0})
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2TkAgg as nav_tool

import matplotlib.ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib.figure import Figure
from matplotlib import gridspec

from engine import Engine

import frames.tests
import frames.batch
import frames.data
import frames.units
import frames.actions
import frames.rejections
import frames.result
import frames.analytical
import frames.export_rejections
import frames.batch_plots

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"

class Biovarase(tk.Frame):
    def __init__(self, engine):
        super().__init__()

        self.master.protocol("WM_DELETE_WINDOW",self.on_exit)

        self.engine = engine
        self.status_bar_text = tk.StringVar()
        self.average = tk.DoubleVar()
        self.bias = tk.DoubleVar()
        self.westgard = tk.StringVar()
        self.calculated_sd = tk.DoubleVar()
        self.calculated_cv = tk.DoubleVar()
        self.range = tk.DoubleVar()
        self.elements = tk.IntVar()
        self.target = tk.DoubleVar()
        self.sd = tk.DoubleVar()
        self.expiration = tk.StringVar()

        self.set_style()
        self.set_icon()
        self.set_title()
        self.center_ui()
        self.init_menu()
        self.init_ui()
        self.init_status_bar()

    def set_style(self):
        self.master.option_readfile('option_db')
        self.master.style = ttk.Style()
        #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        self.master.style.theme_use("clam")        

    def set_icon(self):
        imgicon = tk.PhotoImage(file='biovarase.png')
        self.master.call('wm', 'iconphoto', self.master._w, '-default', imgicon)

    def set_title(self):
        s = "{0} {1}".format(self.engine.title, __version__)
        self.master.title(s)
        #self.winfo_toplevel().title("Biovarase")
        

    def center_ui(self):

        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        # calculate position x, y
        d = self.engine.get_dimensions()
        w = int(d['w'])
        h = int(d['h'])
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def init_menu(self):

        m_main = tk.Menu(self, bd = 1)
               
        m_file = tk.Menu(m_main, tearoff=0, bd = 1)
        s_menu = tk.Menu(m_file)
        m_results = tk.Menu(m_main, tearoff=0, bd = 1)
        m_batches = tk.Menu(m_main, tearoff=0, bd = 1)
        m_about = tk.Menu(m_main, tearoff=0, bd = 1)
        
        m_main.add_cascade(label="File", underline=0, menu=m_file)
        m_main.add_cascade(label="Batches", underline=0, menu=m_batches)
        m_main.add_cascade(label="Results", underline=0, menu=m_results)
        m_main.add_cascade(label="?", underline=0, menu=m_about)


        items = (("Batchs Plots", self.on_batch_plots),
                 ("Reset",self.on_reset),
                 ("Tests",self.on_tests),
                 ("Data",self.on_data),
                 ("Units",self.on_units),
                 ("Actions",self.on_actions),
                 ("Analytica", self.on_analitical),)
        
        for i in items:
            m_file.add_command(label=i[0],underline=0, command=i[1])

        #keep this here
        m_file.add_cascade(label='Export', menu=s_menu, underline=0)

        items = (("Quick Data Analysis", self.engine.get_quick_data_analysis),
                 ("Rejections",self.on_export_rejections),
                 ("Analytical Goals",self.on_analytical_goals),)

        for i in items:
            s_menu.add_command(label=i[0], underline=0, command=i[1])

        m_file.add_separator()
 
        m_file.add_command(label="Exit", underline=0, command=self.on_exit)


        items = (("Add batch", self.on_add_batch),
                 ("Update batch",self.on_update_batch))
        
        for i in items:
            m_batches.add_command(label=i[0],underline=0, command=i[1])
        
        items = (("Add result", self.on_add_result),
                 ("Update result",self.on_update_result))

        for i in items:
            m_results.add_command(label=i[0],underline=0, command=i[1])

        m_about.add_command(label="About",underline=0, command=self.on_about)

        self.master.config(menu=m_main)
                

    def init_ui(self):

        self.pack(fill=tk.BOTH, expand=1,)

        #-----------------------------------------------------------------------
        f0 = self.engine.get_frame(self)

        w = tk.LabelFrame(f0, text='Tests')
        self.cbTests =  ttk.Combobox(w)
        self.cbTests.bind("<<ComboboxSelected>>", self.on_selected_test)
        self.cbTests.pack(side=tk.TOP, fill=tk.X, expand=0)
        w.pack(side=tk.TOP, fill=tk.X, expand=0)

        w = tk.LabelFrame(f0,text='Batchs')
        self.lstBatches = self.engine.get_listbox(w, height=5)
        self.lstBatches.bind("<<ListboxSelect>>", self.on_selected_batch)
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        f1 = tk.Frame(f0,)
        w = tk.LabelFrame(f1,text='Batch data', font='Helvetica 10 bold')

        tk.Label(w, text="Target").pack()
        tk.Label(w, bg='lavender',
                 foreground="blue",
                 textvariable = self.target).pack(fill=tk.X,
                                                  padx=2, pady=2)
        tk.Label(w, text="SD").pack()
        tk.Label(w, bg='lemon chiffon',
                 foreground="green",
                 textvariable = self.sd).pack(fill=tk.X,
                                              padx=2,pady=2)
        tk.Label(w, text="Expiration").pack()
        tk.Label(w, bg='white',
                 textvariable = self.expiration).pack(fill=tk.X,
                                                      padx=2,pady=2)

        self.engine.get_spin_box(w, "Elements",1, 365, 3, self.elements).pack()

        w.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        
        w = tk.LabelFrame(f1,text='Cal data',font='Helvetica 10 bold')
     
        tk.Label(w, text="Average").pack()
        tk.Label(w,  bg='lavender',
                 foreground="blue",
                 textvariable = self.average).pack(fill=tk.X,
                                                   padx=2, pady=2)
        tk.Label(w, text="SD").pack()
        tk.Label(w,  bg='lemon chiffon',
                 foreground="green",
                 textvariable = self.calculated_sd).pack(fill=tk.X,
                                                         padx=2, pady=2)
        tk.Label(w, text="CV%").pack()        
        tk.Label(w, bg='orange3',
                 foreground="white", 
                 textvariable = self.calculated_cv).pack(fill=tk.X,
                                                         padx=2,pady=2)
        tk.Label(w, text="Westgard").pack()

        self.lblWestgard = tk.Label(w,  bg='white', textvariable=self.westgard)
        self.lblWestgard.pack(fill=tk.X, padx=2,pady=2)

        tk.Label(w, text="Bias").pack()
        tk.Label(w,  bg='white', textvariable = self.bias).pack(fill=tk.X, padx=2,pady=2)
        tk.Label(w, text="Range").pack()
        tk.Label(w, bg='white', textvariable = self.range).pack(fill=tk.X, padx=2,pady=2)

        w.pack(side=tk.RIGHT,fill=tk.Y, expand=0)

        f1.pack(side=tk.TOP, fill=tk.Y, expand=0)

        w = tk.LabelFrame(f0,text='Results')
        self.lstResults = self.engine.get_listbox(w,)
        self.lstResults.bind("<<ListboxSelect>>", self.on_selected_result)
        self.lstResults.bind('<Double-Button-1>', self.on_result_activated)
        w.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        
        f0.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        #-----------------------------------------------------------------------
        
        #create graph!
        f2 = tk.Frame(self,)
        #Figure: The top level container for all the plot elements.
        gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1]) 
        fig = Figure()
        fig.suptitle(self.engine.title, fontsize=16)
        fig.subplots_adjust(bottom=0.10, right=0.96, left= 0.06, top=0.88,wspace=0.10)
        self.lj = fig.add_subplot(gs[0], facecolor=('xkcd:light grey'))
        self.frq = fig.add_subplot(gs[1], facecolor=('xkcd:light grey'))
        self.canvas = FigureCanvasTkAgg(fig, f2)
        toolbar = nav_tool(self.canvas, f2)
        toolbar.update()
        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)
        f2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def init_status_bar(self):

        
        self.status = tk.Label(self.master,
                               text = self.engine.title,
                               bd=1,
                               relief=tk.SUNKEN,
                               anchor=tk.W, font='bold')
        self.status.config(fg="blue")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)           

    def on_open(self):

        self.elements.set(self.engine.get_elements())
        self.set_tests()
    
    def on_reset(self):

        self.cbTests.set('')
        self.lstBatches.delete(0, tk.END)
        self.lstResults.delete(0, tk.END)
        self.elements.set(self.engine.get_elements())
        self.set_tests()
        self.reset_batch_data()
        self.reset_cal_data()
        self.reset_graph()

    def reset_graph(self):

        self.lj.clear()
        self.frq.clear()
        self.lj.grid(True)
        self.frq.grid(True)
        self.canvas.draw()
 

    def reset_batch_data(self):
        
        self.expiration.set('')
        self.target.set(0)
        self.sd.set(0)
        
    def reset_cal_data(self):

        self.average.set(0)
        self.calculated_sd.set(0)
        self.calculated_cv.set(0)
        self.bias.set(0)
        self.range.set(0)
        self.westgard.set('No Data')
        self.set_westgard_alarm()

    def set_batch_data(self):

        self.expiration.set(self.selected_batch[3])
        self.target.set(self.selected_batch[4])
        self.sd.set(self.selected_batch[5])

    def set_calculated_data(self, args):

        self.average.set(args[5])
        self.calculated_sd.set(args[6])
        self.calculated_cv.set(args[7])
        self.bias.set(args[8])
        self.range.set(args[9])

    def set_westgard(self,series):
        
        if len(series) > 9:
            rule = self.engine.get_westgard_violation_rule(self.selected_batch[4],
                                             self.selected_batch[5],
                                             series)
        else:
            rule = "No data"
        
        self.westgard.set(rule)
        self.set_westgard_alarm()

    def set_westgard_alarm(self):

        if self.westgard.get() not in("Accept","No data"):
            self.lblWestgard.config(bg="IndianRed1")
        else:
            self.lblWestgard.config(bg="white")           
        
    def set_tests(self):

        index = 0
        self.dict_tests = {}
        voices = []
       
        sql = "SELECT tests.test_id,tests.test||' '||samples.sample\
               FROM tests\
               INNER JOIN samples ON tests.sample_id = samples.sample_id\
               WHERE tests.enable=1\
               ORDER BY tests.test"
        
        rs = self.engine.read(True, sql, ())

        for i in rs:
            self.dict_tests[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbTests['values'] = voices        
        self.reset_batch_data()
        
    def set_batches(self):

        self.lstBatches.delete(0, tk.END)
        self.lstResults.delete(0, tk.END)

        index = 0
        self.dict_batchs = {}
        sql = "SELECT * FROM lst_batches WHERE test_id = ?"
        rs = self.engine.read(True, sql, (self.selected_test[0],))
        
        if rs:
            for i in rs:
                s = "%s"%(i[1])
                self.lstBatches.insert(tk.END, (s))
                self.dict_batchs[index] = i[0]
                index += 1

            self.lstBatches.select_set(0)
            self.lstBatches.event_generate("<<ListboxSelect>>")
        else:
            
            self.reset_cal_data()
            self.reset_graph() 
            

    def set_results(self,):

        try:
            self.lstResults.delete(0, tk.END)
            index = 0
            self.dict_results = {}
           
            sql = "SELECT * FROM lst_results WHERE batch_id = ? LIMIT ?"
            rs = self.engine.read(True, sql, (self.selected_batch[0],int(self.elements.get())))
            
            target = float(self.selected_batch[4])
            sd = float(self.selected_batch[5])
    
            if rs:

                for i in rs:

                    s = '{}{:10}'.format(i[2],i[1])
                    self.lstResults.insert(tk.END, s)

                    result = float(round(i[1],2))

                    is_enabled = i[4]
        
                    self.set_results_row_color(index, result, is_enabled, target, sd)
                    
                    self.dict_results[index]=i[0]
                   
                    index+=1

                self.get_values(rs) 
                
            else:
                self.reset_cal_data()
                self.reset_graph()

        except:
            
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            print(self.selected_batch[0])
            
            
    def on_selected_test(self,event):

        if self.cbTests.current()!=-1:
            index = self.cbTests.current()
            pk = self.dict_tests[index]
            self.selected_test = self.engine.get_selected('lst_tests','test_id', pk)
            self.reset_batch_data()
            self.reset_cal_data()
            self.set_batches()
    
    def on_selected_batch(self,event):

        if self.lstBatches.curselection():

            index = self.lstBatches.curselection()[0]
            pk = self.dict_batchs.get(index)
            self.selected_batch = self.engine.get_selected('batches','batch_id', pk)
            
            self.set_batch_data()
            self.set_results()

    def on_selected_result(self,event):

        if self.lstResults.curselection():
            
            index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(index)
            self.selected_result = self.engine.get_selected('results','result_id', pk)            

    def on_result_activated(self, event):

        if self.lstResults.curselection():
                index = self.lstResults.curselection()[0]
                obj = frames.rejections.Dialog(self, self.engine,)
                obj.on_open(self.selected_test, self.selected_batch, self.selected_result)
                
          
    def set_results_row_color(self, index, result, is_enabled, target, sd):

        if is_enabled == 0:
            self.lstResults.itemconfig(index, {'bg':'light gray'})
        else:
            d = {}
            if result >= target:
                #result > 3sd
                if result >= (target + (sd*3)):
                    d['bg']='red'
                #if result is > 2sd and < +3sd
                elif result >= (target + (sd*2)) and result <= (target + (sd*3)):
                    d['bg']='yellow'
                    
            elif result <= target:                
                #result < 3sd
                if result <= (target - (sd*3)):
                    d['bg']='red'
                #if result is > -2sd and < -3sd
                elif result <= (target - (sd*2)) and result >= (target - (sd*3)):
                    d['bg']='yellow'
                    
            self.lstResults.itemconfig(index, d)                    
               
        
                
    def get_um(self,):

        sql = "SELECT unit FROM lst_tests WHERE test_id =?"
        return self.engine.read(False, sql, (self.selected_test[0],))


    def get_values(self, rs):

        """args = self.engine.get_qc(self.selected_batch, rs)
            args = (0, count_rs,
                    1, target,
                    2, sd,
                    3, series,
                    4, count_series,
                    5, compute_average,
                    6, compute_sd,
                    7, compute_cv,
                    8, compute_bias,
                    9, compute_range,
                    10, x_labels,
                    11, dates)   
            """
        args = self.engine.get_qc(self.selected_batch, rs)
        if args is not None:
            self.set_calculated_data(args)
            self.set_westgard(args[3])
            self.set_lj(args[0],
                        args[1],
                        args[2],
                        args[3],
                        args[4],
                        args[5],
                        args[6],
                        args[7],
                        args[10],
                        args[11],)

            self.set_histogram(args[3],
                               args[1],
                               args[5],
                               args[2],
                               args[7],
                               args[6])
                
            self.canvas.draw()
            
        else:
            self.reset_cal_data()
            self.reset_graph()

    def set_lj(self, count_rs, target, sd, series, count_series,
               compute_average, compute_sd, compute_cv, x_labels, dates):

        self.lj.clear()
        self.lj.grid(True)
        um = self.get_um()
        lines = ([],[],[],[],[],[],[])

        for i in range(len(series)+1):

            lines[0].append(target+(sd*3))
            lines[1].append(target+(sd*2))
            lines[2].append(target+sd)

            lines[3].append(target)

            lines[4].append(target-sd)
            lines[5].append(target-(sd*2))
            lines[6].append(target-(sd*3))
        
        #it's show time
        self.lj.set_xticks(range(0, len(series)+1))
        self.lj.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(21))
        self.lj.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        self.lj.set_xticklabels(x_labels, rotation=70, size=6)
        self.lj.plot(series, marker="8", label='data')
             
        for x,y in enumerate(series):
            self.lj.text(x, y, str(y),)
            
        self.lj.plot(lines[0],color="red",label='+3 sd',linestyle='--')
        self.lj.plot(lines[1],color="yellow",label='+2 sd',linestyle='--')
        self.lj.plot(lines[2],color="green",label='+1 sd',linestyle='--')
        self.lj.plot(lines[3],label='target', linewidth=2)
        self.lj.plot(lines[4],color="green",label='-1 sd',linestyle='--')
        self.lj.plot(lines[5],color="yellow",label='-2 sd',linestyle='--')
        self.lj.plot(lines[6],color="red",label='-3 sd',linestyle='--')

        if um is  not None:
            self.lj.set_ylabel(str(um[0]))
        else:
            self.lj.set_ylabel("No unit assigned yet")

        
        s = "{0} Batch: {1} Target: {2} SD: {3} Exp: {4}".format(self.selected_test[1],
                                                         self.selected_batch[2],
                                                         self.selected_batch[4],
                                                         self.selected_batch[5],
                                                         self.selected_batch[3],)
        
        self.lj.set_title(s, weight='bold',loc='left')

        
        bottom_text = (self.format_interval_date(dates), count_series, count_rs)

        self.lj.text(0.95, 0.01,
                     '%s computed %s on %s results'%bottom_text,
                     verticalalignment='bottom',
                     horizontalalignment='right',
                     transform=self.lj.transAxes,
                     color='black',weight='bold')

    def set_histogram(self, series, target, avg, sd, cv, compute_sd):

        #histogram of frequency distribuition
        self.frq.clear()
        self.frq.grid(True)
        self.frq.hist(series, color='g')
        self.frq.axvline(target, color='orange',linewidth=2)
        self.frq.axvline(avg, color='b',linewidth=2)
        self.frq.set_ylabel('Frequency')
        title = "avg = %.2f,  std = %.2f cv = %.2f" % (avg, compute_sd, cv)
        self.frq.set_title(title)
        um = self.get_um()
        if um is  not None:
            self.frq.set_xlabel(str(um[0]))
        else:
            self.frq.set_xlabel("No unit assigned yet")
         

    def format_interval_date(self,dates):

        try:

            x = min(dates)
            s1 = "%s-%s-%s" %(x.day,x.month,x.year)
            x = max(dates)
            s2 = "%s-%s-%s" %(x.day,x.month,x.year)
                
            return  "from %s to %s"%(s1,s2)

        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])


    def on_analytical_goals(self):

        sql = "SELECT batches.batch_id,\
                         samples.sample,\
                      tests.test,\
                      batches.batch,\
                      batches.expiration,\
                      batches.target,\
                      tests.cvw,\
                      tests.cvb\
               FROM tests\
               INNER JOIN samples \
               ON tests.sample_id = samples.sample_id\
               INNER JOIN batches \
               ON tests.test_id = batches.test_id\
               WHERE tests.enable = 1\
               AND tests.cvw !=0\
               AND tests.cvb !=0\
               AND batches.target !=0\
               AND batches.enable = 1\
               ORDER BY tests.test,samples.sample"

        limit = int(self.elements.get())
        rs = self.engine.read(True, sql, ())

        if rs:
            self.engine.get_analitical_goals(limit,rs)
        else:
            msg = "No record data to compute analytical goals."
            messagebox.showwarning(self.engine.title,msg)
            
    def on_tests(self,):
        
        f = frames.tests.Dialog(self,self.engine)
        f.on_open()

    def on_units(self,):
        
        f = frames.units.Dialog(self,self.engine)
        f.on_open()           

    def on_data(self,):
        
        f = frames.data.Dialog(self,self.engine)
        f.on_open()

    def on_actions(self,):
        f = frames.actions.Dialog(self,self.engine)
        f.on_open()

    def on_analitical(self,):

        f = frames.analytical.Dialog(self,self.engine)
        f.on_open()

    def on_export_rejections(self,):
        f = frames.export_rejections.Dialog(self,self.engine)
        f.on_open()

    def on_batch_plots(self,):

        if self.cbTests.current() != -1:
            index = self.cbTests.current()
            pk = self.dict_tests[index]
            selected_test = self.engine.get_selected('lst_tests','test_id', pk)
            f = frames.batch_plots.Dialog(self,self.engine)
            f.on_open(selected_test,int(self.elements.get()))
        else:
            msg = "Not enough data to plot.\nSelect a test."
            messagebox.showwarning(self.engine.title,msg)        
        
        
    def on_add_batch(self):

        if self.cbTests.current() != -1:
            obj = frames.batch.Dialog(self,self.engine,)
            obj.transient(self)
            obj.on_open(self.selected_test)

        else:
            msg = "Attention please.\nBefore add a batch you must select a test."
            messagebox.showinfo(self.engine.title, msg)            

    def on_update_batch(self):

        if self.lstBatches.curselection():
            index = self.lstBatches.curselection()[0]
            obj = frames.batch.Dialog(self, self.engine, index)
            obj.transient(self)
            obj.on_open(self.selected_test, self.selected_batch)
        else:
            msg = "Attention please.\nSelect a batch."
            messagebox.showinfo(self.engine.title, msg)            


    def on_add_result(self,):

        if self.selected_batch is not None:
            obj = frames.result.Dialog(self, self.engine,)
            obj.on_open(self.selected_test, self.selected_batch)
        else:
            msg = "Attention please.\nBefore add a result you must select a batch."
            messagebox.showinfo(self.engine.title, msg)

    def on_update_result(self,):

        try:
            if self.lstResults.curselection():
                index = self.lstResults.curselection()[0]
                obj = frames.result.Dialog(self, self.engine, index)
                obj.on_open(self.selected_test, self.selected_batch, self.selected_result)

            else:
                msg = "Attention please.\nSelect a result."
                messagebox.showinfo(self.engine.title, msg)                
                
        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])

 
    def on_about(self,):
        messagebox.showinfo(self.engine.title, self.engine.about)        
  
    def on_exit(self):
        """Close all"""
        if messagebox.askokcancel(self.engine.title, "Do you want to quit?"):
            self.engine.con.close()
            self.master.quit()
            
def main():

    app = Biovarase(Engine())
    app.on_open()
    app.mainloop()

   
if __name__ == '__main__':
    main()
