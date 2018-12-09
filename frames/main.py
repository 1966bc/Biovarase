#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn 2018                                                        
#-----------------------------------------------------------------------------
import os
import sys
import inspect
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import numpy as np

import matplotlib.pyplot as plt

plt.rcParams.update({'figure.max_open_warning': 0})
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2TkAgg as nav_tool

import matplotlib.ticker
from matplotlib.ticker import LinearLocator
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

class Biovarase(Frame):
    def __init__(self, engine):
        super().__init__()

        self.engine = engine
        self.master.protocol("WM_DELETE_WINDOW",self.on_exit)
        self.average = DoubleVar()
        self.bias = DoubleVar()
        self.westgard = StringVar()
        self.calculated_sd = DoubleVar()
        self.calculated_cv = DoubleVar()
        self.range = DoubleVar()
        self.elements = IntVar()
        self.target = DoubleVar()
        self.sd = DoubleVar()
        self.expiration = StringVar()
        self.init_menu()
        self.init_ui()
        self.init_status_bar()

    def init_menu(self):

        m_main = Menu(self, bd = 1)
               
        m_file = Menu(m_main, tearoff=0, bd = 1)
        s_menu = Menu(m_file)
        m_results = Menu(m_main, tearoff=0, bd = 1)
        m_batches = Menu(m_main, tearoff=0, bd = 1)
        m_about = Menu(m_main, tearoff=0, bd = 1)
        
        m_main.add_cascade(label="File", underline=0, menu=m_file)
        m_main.add_cascade(label="Batches", underline=0, menu=m_batches)
        m_main.add_cascade(label="Results", underline=0, menu=m_results)
        m_main.add_cascade(label="?", underline=0, menu=m_about)


        items = (("Reset",self.on_reset),
                 ("Tests",self.on_tests),
                 ("Data",self.on_data),
                 ("Units",self.on_units),
                 ("Actions",self.on_actions),)
        
        for i in items:
            m_file.add_command(label=i[0],underline=0, command=i[1])

        #keep this here
        m_file.add_cascade(label='Export', menu=s_menu, underline=0)

        items = (("Quick Data Analysis", self.engine.get_quick_data_analysis),
                 ("Rejections",self.engine.get_rejections),
                 ("Analytical Goals",self.set_analytical_goals),)

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

        self.pack(fill=BOTH, expand=1,)

        #-----------------------------------------------------------------------
        f0 = Frame(self,bd=5)

        w = LabelFrame(f0, text='Tests')
        self.cbTests =  ttk.Combobox(w)
        self.cbTests.bind("<<ComboboxSelected>>", self.on_selected_test)
        self.cbTests.pack(side=TOP,fill=X,expand=0)
        w.pack(side=TOP,fill=X, expand=0)

        w = LabelFrame(f0,text='Batchs')
        self.lstBatches = self.engine.get_listbox(w, height=5)
        self.lstBatches.bind("<<ListboxSelect>>", self.on_selected_batch)
        w.pack(side=TOP,fill=BOTH, expand=0)

        f1 = Frame(f0,bd=5)
        w = LabelFrame(f1,text='Batch data', font='Helvetica 10 bold')

        Label(w, text="Target").pack()
        Label(w, bg='lavender',foreground="blue", textvariable = self.target).pack(fill=X, padx=2,pady=2)
        Label(w, text="SD").pack()
        Label(w, bg='lemon chiffon', foreground="green", textvariable = self.sd).pack(fill=X, padx=2,pady=2)
        Label(w, text="Expiration").pack()
        Label(w, bg='white', textvariable = self.expiration).pack(fill=X, padx=2,pady=2)

        self.engine.get_spin_box(w, "Elements",1, 365, 3, self.elements).pack()

        w.pack(side=LEFT, fill=Y, expand=0)
        
        w = LabelFrame(f1,text='Cal data',font='Helvetica 10 bold')
     
        Label(w, text="Average").pack()
        Label(w,  bg='lavender', foreground="blue", textvariable = self.average).pack(fill=X, padx=2, pady=2)
        Label(w, text="SD").pack()
        Label(w,  bg='lemon chiffon', foreground="green", textvariable = self.calculated_sd).pack(fill=X, padx=2, pady=2)
        Label(w, text="CV%").pack()        
        Label(w, foreground="white", bg='orange3', textvariable = self.calculated_cv).pack(fill=X, padx=2,pady=2)
        Label(w, text="Westgard").pack()

        self.lblWestgard = Label(w,  bg='white', textvariable = self.westgard)
        self.lblWestgard.pack(fill=X, padx=2,pady=2)

        Label(w, text="Bias").pack()
        Label(w,  bg='white', textvariable = self.bias).pack(fill=X, padx=2,pady=2)
        Label(w, text="Range").pack()
        Label(w, bg='white', textvariable = self.range).pack(fill=X, padx=2,pady=2)

        w.pack(side=RIGHT,fill=Y, expand=0)

        f1.pack(side=TOP, fill=Y, expand=0)

        w = LabelFrame(f0,text='Results')
        self.lstResults = self.engine.get_listbox(w,)
        self.lstResults.bind("<<ListboxSelect>>", self.on_selected_result)
        self.lstResults.bind('<Double-Button-1>', self.on_result_activated)
        w.pack(side=TOP,fill=BOTH, expand=1)
        
        f0.pack(side=LEFT, fill=Y, expand=0)
        #-----------------------------------------------------------------------
        
        #create graph!
        f2 = Frame(self,bd=5,)
        f2.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
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
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    def init_status_bar(self):

        s = "%s %s"%(self.engine.title, self.engine.get_version())
        self.status = Label(self.master, text = s.strip(), bd=1, relief=SUNKEN, anchor=W, font='bold')
        self.status.config(fg="blue")
        self.status.pack(side=BOTTOM, fill=X)           

    def on_open(self):

        self.elements.set(self.engine.get_elements())
        self.on_reset()
    
    def on_reset(self):
        
        self.selected_batch = None
        self.lstBatches.delete(0, END)
        self.lstResults.delete(0, END)
        self.cbTests.set('')
        self.set_tests()
        self.reset_graph()

    def reset_graph(self):
        try:
            self.lj.clear()
            self.frq.clear()
            self.lj.grid(True)
            self.frq.grid(True)
            self.canvas.draw()
        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])

    def reset_batch_data(self):
        
        self.expiration.set('')
        self.target.set(0)
        self.sd.set(0)
        
    def reset_cal_data(self):

        self.average.set(0)
        self.bias.set(0)
        self.westgard.set('No Data')
        self.calculated_sd.set(0)
        self.calculated_cv.set(0)
        self.range.set(0)
        self.set_westgard_alarm()
        
    def set_tests(self):

        index = 0
        self.dict_tests={}
        v = []
       
        sql = "SELECT tests.test_id,tests.test||' '||samples.sample\
               FROM tests\
               INNER JOIN samples ON tests.sample_id = samples.sample_id\
               WHERE tests.enable=1\
               ORDER BY tests.test"
        
        rs = self.engine.read(True, sql, ())

        for i in rs:
            self.dict_tests[index]=i[0]
            index+=1
            v.append(i[1])

        self.cbTests['values']=v        
        self.reset_batch_data()
        
    def set_batches(self):

        self.lstBatches.delete(0, END)
        self.lstResults.delete(0, END)

        index = 0
        self.dict_batchs={}
        sql = "SELECT * FROM lst_batchs WHERE test_id = ?"
        rs = self.engine.read(True, sql, (self.selected_test[0],))
        
        if rs:
            for i in rs:
                s = "%s"%(i[1])
                self.lstBatches.insert(END, (s))
                self.dict_batchs[index]=i[0]
                index+=1

            self.lstBatches.select_set(0)
            self.lstBatches.event_generate("<<ListboxSelect>>")
        else:
            
            self.reset_cal_data()
            self.reset_graph() 
            

    def set_results(self,):

        try:
            self.lstResults.delete(0, END)
            index = 0
            self.dict_results={}
           
            sql = "SELECT * FROM lst_results WHERE batch_id = ? LIMIT ?"
            rs = self.engine.read(True, sql, (self.selected_batch[0],int(self.elements.get())))
            
            target = float(self.selected_batch[4])
            sd = float(self.selected_batch[5])
    
            if rs:

                for i in rs:

                    s = '{}{:10}'.format(i[2],i[1])
                    self.lstResults.insert(END, s)

                    result = float(i[1])

                    is_enabled = i[4]
        
                    self.set_results_row_color(index, result, is_enabled, target, sd)
                    
                    self.dict_results[index]=i[0]
                   
                    index+=1

                #check if it exists at least a value with the equal enable = 1
                #if values don't exist we cannot compute stat.
                if self.engine.get_dataset(rs):
                    self.get_data(rs, target, sd)
                else:
                    self.reset_cal_data()
                    self.reset_graph()
                
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
            self.selected_batch = self.engine.get_selected('batchs','batch_id', pk)
            
            self.set_batch()
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
                
    def set_batch(self):

        s = "{0} {1}".format(self.selected_test[1],self.selected_batch[2])
        
        self.expiration.set(self.selected_batch[3])
        self.target.set(self.selected_batch[4])
        self.sd.set(self.selected_batch[5])
           
                         
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
               
    def set_westgard(self,series):

        if len(series) > 9:
            rule = self.engine.get_violation(self.selected_batch[4],self.selected_batch[5],series)
        else:
            rule = "No data"
        
        self.westgard.set(rule)
        self.set_westgard_alarm()

    def set_westgard_alarm(self):

        if self.westgard.get() not in("Accept","No data"):
            self.lblWestgard.config(bg="IndianRed1")
        else:
            self.lblWestgard.config(bg="white")        
                
    def get_um(self,):

        sql = "SELECT unit FROM lst_tests WHERE test_id =?"
        return self.engine.read(False, sql, (self.selected_test[0],))


    def get_data(self, rs, target, sd):

        um = self.get_um()
        series = []
        dates = []
        x_labels = []
        count_rs = len(rs)
        #compute record with enable = 1
        #check if it exists at least a value with the equal enable = 1
        #if values don't exist we cannot compute stat.
        rs = self.engine.get_dataset(rs)

        for i in reversed(rs):
            series.append(i[1])
            x_labels.append(i[2])
            dates.append(i[3])

        count_series = len(series)

        if rs:

            compute_average = round(np.mean(series),2)
            compute_sd = round(np.std(series),2)
            compute_cv = round((compute_sd/compute_average)*100,2)
            self.average.set(compute_average)
            self.calculated_sd.set(compute_sd)
            self.calculated_cv.set(compute_cv)
            self.bias.set(round((compute_average-target)/(target)*100,2))
            self.set_westgard(series)
            self.range.set(round(np.ptp(series),2))

            self.set_lj(series,
                        target,
                        compute_average,
                        sd,
                        compute_cv,
                        um,
                        x_labels,
                        dates,
                        count_rs,
                        count_series)
                
            self.set_histogram(series,
                               target,
                               compute_average,
                               sd,
                               compute_cv,
                               um,
                               compute_sd)
            self.canvas.draw()

        
        else:
            self.reset_cal_data()
            self.reset_graph()
      

    def set_lj(self, series, target, avg, sd, cv, um, x_labels, dates, count_rs, count_series):

        self.lj.clear()
        self.lj.grid(True)

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

        text_data = (self.format_interval_date(dates), count_rs, count_series)

        self.lj.text(0.95, 0.01,
                     '%s computed %s on %s results'%text_data,
                     verticalalignment='bottom',
                     horizontalalignment='right',
                     transform=self.lj.transAxes,
                     color='black',weight='bold')

    def set_histogram(self, series, target, avg, sd, cv, um, compute_sd):

        #histogram of frequency distribuition
        self.frq.clear()
        self.frq.grid(True)
        self.frq.hist(series, color='g')
        self.frq.axvline(target, color='orange',linewidth=2)
        self.frq.axvline(avg, color='b', linestyle='dashed', linewidth=2)
        self.frq.set_ylabel('Frequency')
        title = "avg = %.2f,  std = %.2f cv = %.2f" % (avg, compute_sd, cv)
        self.frq.set_title(title)
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


    def set_analytical_goals(self):

        sql = "SELECT batchs.batch_id,\
                         samples.sample,\
                      tests.test,\
                      batchs.batch,\
                      batchs.expiration,\
                      batchs.target,\
                      tests.cvw,\
                      tests.cvb\
               FROM tests\
               INNER JOIN samples \
               ON tests.sample_id = samples.sample_id\
               INNER JOIN batchs \
               ON tests.test_id = batchs.test_id\
               WHERE tests.enable = 1\
               AND tests.cvw !=0\
               AND tests.cvb !=0\
               AND batchs.target !=0\
               AND batchs.enable = 1\
               ORDER BY tests.test,samples.sample"

        limit = int(self.elements.get())
        rs = self.engine.read(True, sql, ())

        if rs:
            self.engine.get_analytical_goals(limit,rs)
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
            obj = frames.batch.Dialog(self,self.engine, index)
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
            self.master.quit()
            
def main():

   
    engine = Engine()
    root = Tk()
    root.option_readfile('option_db')
    root.style = ttk.Style()
    #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    root.style.theme_use("clam")
    #set icon
    imgicon = PhotoImage(file='biovarase.png')
    root.call('wm', 'iconphoto', root._w, '-default', imgicon)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    #root.geometry("{0}x{1}+0+0".format(1200, 600))
    root.title(engine.title)
    app = Biovarase(engine)
    app.on_open()
    root.mainloop()
  
if __name__ == '__main__':
    main()
