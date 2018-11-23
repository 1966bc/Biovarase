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
import datetime

import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2TkAgg as nav_tool

import matplotlib.ticker
from matplotlib.ticker import LinearLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.figure import Figure

from engine import Engine

import frames.tests
import frames.batch 
import frames.batchs
import frames.units

class Biovarase(Frame):
    def __init__(self, engine):
        super().__init__()

        self.engine = engine
        self.master.protocol("WM_DELETE_WINDOW",self.on_exit)
        self.selected_data = StringVar()
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
        self.ax = None
        
        self.init_menu()
        self.init_ui()
        self.init_status_bar()

    def init_menu(self):

        m_main = Menu(self, bd = 1)
        
        m_file = Menu(m_main, tearoff=0, bd = 1)
        m_about = Menu(m_main, tearoff=0, bd = 1)
        
        m_main.add_cascade(label="File", underline=1, menu=m_file)
        m_main.add_cascade(label="?", underline=0, menu=m_about)

        items = (("Quick Data Analysis", self.on_quick_data_analysis),
                 ("Reset",self.on_reset),
                 ("Export",self.on_export),
                 ("Tests",self.on_tests),
                 ("Batchs",self.batchs),
                 ("Units",self.on_units),
                 ("Exit",self.on_exit),)

        for i in items:
            m_file.add_command(label=i[0],underline=0, command=i[1])

        m_about.add_command(label="About",underline=0, command=self.on_about)
     
        self.master.config(menu=m_main)        
        
    def init_ui(self):

        self.pack(fill=BOTH, expand=1,)

        #-----------------------------------------------------------------------
        f0 = Frame(self, bd=5)

        w = LabelFrame(f0, text='Tests')
        self.cbTests =  ttk.Combobox(w)
        self.cbTests.bind("<<ComboboxSelected>>", self.on_selected_test)
        self.cbTests.pack(side=TOP,fill=X,expand=0)
        w.pack(side=TOP,fill=X, expand=0)

        w = LabelFrame(f0, text='Batchs')
        self.lstBatchs = self.engine.get_listbox(w,)
        self.lstBatchs.bind("<<ListboxSelect>>", self.on_selected_batch)
        self.lstBatchs.bind('<Button-3>', self.on_batch_activated)
        w.pack(side=TOP,fill=BOTH, expand=0)
       
        w = LabelFrame(f0,text='Results')
        self.lstResults = self.engine.get_listbox(w,)
        self.lstResults.bind("<<ListboxSelect>>", self.on_selected_result)
        self.lstResults.bind('<Double-Button-1>', self.on_enable_result)
        w.pack(side=TOP,fill=BOTH, expand=1)
        
        f0.pack(side=LEFT, fill=Y, expand=0)

        #-----------------------------------------------------------------------
        f1 = Frame(self,bd=5)
        w = LabelFrame(f1,text='Selected batch data', font='Helvetica 10 bold')

        Label(w, text="Target").pack()
        Label(w, bg='lavender',foreground="blue", textvariable = self.target).pack(fill=X, padx=2,pady=2)
        Label(w, text="Standard Deviation").pack()
        Label(w, bg='lemon chiffon', foreground="green", textvariable = self.sd).pack(fill=X, padx=2,pady=2)
        Label(w, text="Expiration").pack()
        Label(w, bg='white', textvariable = self.expiration).pack(fill=X, padx=2,pady=2)
        Label(w, text="Elements").pack()

        self.spElements = Spinbox(w,
                                  bg='white',
                                  from_=1,
                                  to=365,
                                  justify=CENTER,
                                  width=3,
                                  wrap=True,
                                  insertwidth=1,
                                  textvariable=self.elements)
        self.spElements.pack(fill=X, expand=0)

        w.pack(side=TOP, fill=X, expand=0)

        f1.pack(side=LEFT, fill=Y, expand=0)

        #-----------------------------------------------------------------------
        f2 = Frame(self,bd=5)

        w = LabelFrame(f2,text='Calculated data',font='Helvetica 10 bold')
     
        Label(w, text="Average").pack()
        Label(w,  bg='lavender', foreground="blue", textvariable = self.average).pack(fill=X, padx=2, pady=2)
        Label(w, text="Standard Deviation").pack()
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

        w.pack(side=TOP,fill=X, expand=0)

        f2.pack(side=LEFT, fill=Y, expand=0)
 
        self.Frame_Graph = Frame(self,bd=5,)

        lbl = Label(self.Frame_Graph,font='Helvetica 18 bold italic',foreground="Blue", textvariable = self.selected_data)
        lbl.pack()
       
        self.Frame_Graph.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)

        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor('xkcd:light grey')
        self.ax.set_axisbelow(True)
        self.ax.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(21))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        self.line = self.ax.plot()
        self.canvas = FigureCanvasTkAgg(fig,self.Frame_Graph)
        toolbar = nav_tool(self.canvas, self.Frame_Graph)
        toolbar.update()
        #self.canvas.show()
        #self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    def init_status_bar(self):
        
        self.status = Label(self.master, text = self.engine.title, bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)           

    def on_open(self):

        self.set_elements()
        self.on_reset()
    
    def set_elements(self):
        
        self.elements.set(self.engine.get_elements())
    
    def on_reset(self):
        
        self.selected_batch = None
        self.lstBatchs.delete(0, END)
        self.lstResults.delete(0, END)
        self.cbTests.set('')
        self.set_tests()
        self.reset_graph()
       

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
        
        self.reset_texts()
        

    def set_batchs(self):

        index = 0
        self.dict_batchs={}
        sql = "SELECT * FROM lst_batchs WHERE test_id = ?"
        rs = self.engine.read(True, sql, (self.selected_test[0],))
        
        if rs:
            for i in rs:
                s = "%s"%(i[1])
                self.lstBatchs.insert(END, (s))
                self.dict_batchs[index]=i[0]
                index+=1

            self.lstBatchs.select_set(0)
            self.lstBatchs.event_generate("<<ListboxSelect>>")

    def set_results(self,):           
            
            self.lstResults.delete(0, END)

            index = 0
            self.dict_results={}
           

            sql = "SELECT * FROM lst_results WHERE batch_id = ? LIMIT ?"
            rs = self.engine.read(True, sql, (self.selected_batch[0],int(self.spElements.get())))

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

                series = self.get_series(rs)                 
                avg = round(np.mean(series),2)
                sd = round(np.std(series),2)
                self.average.set(avg)
                self.bias.set(round((avg-target)/(target)*100,2))
                self.set_westgard(series)
                self.calculated_sd.set(sd)
                self.calculated_cv.set(round((sd/avg)*100,2))
                self.range.set(round(np.ptp(series),2))
                self.set_graph(rs)
                
            else:
                self.westgard.set('No Data')
                self.calculated_sd.set(0)
                self.calculated_cv.set(0)
                self.range.set(0)
                self.reset_graph()            

    def reset_graph(self):
            try:
                if self.ax is not None:
                    self.selected_data.set('Biovarase')
                    self.ax.clear()
                    self.ax.grid()
                    self.canvas.draw()
            except:
                print(inspect.stack()[0][3])
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])

    def reset_texts(self):
        
        self.selected_data.set('')
        self.expiration.set('')
        self.target.set(0)
        self.sd.set(0)
        self.average.set(0)
        self.bias.set(0)
        self.westgard.set('No Data')
        self.calculated_sd.set(0)
        self.calculated_cv.set(0)
        self.range.set(0)
        self.set_westgard_alarm()
        

    def on_selected_test(self,event):

        index = self.cbTests.current()
        test_id = self.dict_tests[index]
        self.selected_test = self.engine.get_selected('lst_tests','test_id', test_id)
        
        self.lstBatchs.delete(0, END)
        self.lstResults.delete(0, END)
        self.reset_texts()
        self.selected_data.set(self.selected_test[1])
        self.set_batchs()
    
            
    def on_selected_batch(self,event):

        if self.lstBatchs.curselection():

            index = self.lstBatchs.curselection()[0]
            pk = self.dict_batchs.get(index)
            self.selected_batch = self.engine.get_selected('batchs','batch_id', pk)
            self.batch_index = index
            self.set_qc_data()
            self.set_results()

    def on_batch_activated(self, event):

        if self.lstBatchs.curselection():
            self.obj = frames.batch.Dialog(self,self.engine,)
            self.obj.transient(self)
            self.obj.on_open(self.selected_test, self.selected_batch)

    def on_selected_result(self,event):

        if self.lstResults.curselection():
            
            index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(index)
            self.selected_result = self.engine.get_selected('results','result_id', pk)

    def on_enable_result(self, event):

        try:
            if self.lstResults.curselection():

                index = self.lstResults.curselection()[0]
                pk = self.dict_results.get(index)
                sql = "SELECT enable FROM results WHERE result_id =?"
                rs = self.engine.read(False, sql, (pk,))
                if rs[0] == 0:
                    sql = "UPDATE results SET enable=1 WHERE result_id=?"
                else:
                    sql = "UPDATE results SET enable=0 WHERE result_id=?"

                self.engine.write(sql, (pk,))
                self.set_results()
                
        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])             
            

    def set_qc_data(self):

        s = "{0} {1}".format(self.selected_test[1],self.selected_batch[2])
        self.selected_data.set(s)

        self.expiration.set(self.selected_batch[3])
        self.target.set(self.selected_batch[4])
        self.sd.set(self.selected_batch[5])

    def get_series(self, rs):

        """return a value series to compute stat data
           notice that i[4] is enable field of the resultset
       
        @param name: rs
        @return: a value series
        @rtype: list
        """     
        series = []

        rs = tuple(i for i in rs if i[4]!=0)

        for i in rs:
            series.append(i[1])

        return series             
                         
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

        sql = "SELECT unit FROM units WHERE unit_id =?"
        return self.engine.read(False, sql, (self.selected_test[3],))


    def set_graph(self, rs_results):

        if self.selected_batch is not None :

            all_data = len(rs_results)
            #compute record with enable = 1
            rs = tuple(i for i in rs_results if i[4]!=0)
            compute_data = len(rs)
            
            if rs is not None:

                if compute_data<3:
                    msg = ("%s : lot %s INSUFFICIENT DATA FOR MEANINGFUL ANSWER"% (self.selected_test[2],self.selected_batch[2]))
                else:
                    
                    target = self.selected_batch[4]
                    sd = self.selected_batch[5]
                    data = []
                    dates = []
                    x_labels = []

                    for i in reversed(rs):
                        
                        data.append(i[1])
                        x_labels.append(i[2])
                        dates.append(i[3])

                    avg = round(np.mean(data),2)
                    sd = round(np.std(data),2)
                    cv = round((sd/avg)*100,2)

                    target_line = []
                    sd1line = []
                    sd2line = []
                    sd3line = []
                    sd1_line = []
                    sd2_line = []
                    sd3_line = []

                    for i in range(len(data)+1):
                      
                        sd1line.append(self.selected_batch[4]+self.selected_batch[5])
                        sd2line.append(self.selected_batch[4]+(self.selected_batch[5]*2))
                        sd3line.append(self.selected_batch[4]+(self.selected_batch[5]*3))
                        sd1_line.append(self.selected_batch[4]-self.selected_batch[5])
                        sd2_line.append(self.selected_batch[4]-(self.selected_batch[5]*2))
                        sd3_line.append(self.selected_batch[4]-(self.selected_batch[5]*3))
                        target_line.append(self.selected_batch[4])

                    try:
                        #it's show time
                        self.ax.clear()
                        self.ax.grid()
                        self.ax.set_xticks(range(0, len(data)+1))
                        self.ax.set_xticklabels(x_labels, rotation=70, size=6)
                        self.ax.plot(data, marker="8", label='data')
                         
                        for x,y in enumerate(data):
                            self.ax.text(x, y, str(y),)

                        self.ax.plot(target_line,label='target', linewidth=2)
                        self.ax.legend(loc='upper right')
                        self.ax.plot(sd1line,color="green",label='+1 sd',linestyle='--')
                        self.ax.plot(sd2line,color="yellow",label='+2 sd',linestyle='--')
                        self.ax.plot(sd3line,color="red",label='+3 sd',linestyle='--')
                        self.ax.plot(sd1_line,color="green",label='-1 sd',linestyle='--')
                        self.ax.plot(sd2_line,color="yellow",label='-2 sd',linestyle='--')
                        self.ax.plot(sd3_line,color="red",label='-3 sd',linestyle='--')
  
                        um = self.get_um()
                        if um is  not None:
                            self.ax.set_ylabel(str(um[0]))
                        else:
                            self.ax.set_ylabel("No unit assigned yet")

                        msg = "Test: %s Batch: %s Expiration: %s " %(self.selected_test[1],
                                                                     self.selected_batch[2],
                                                                     self.selected_batch[3],)
                        self.ax.set_title(msg)

                        text_data = (avg,sd,cv,self.format_interval_date(dates), compute_data, all_data)

                        self.ax.text(0.95, 0.01,
                                 'avg:%s sd:%s cv:%s %s computed %s on %s results'%text_data,
                                 verticalalignment='bottom',
                                 horizontalalignment='right',
                                 transform=self.ax.transAxes,
                                 color='black')
                            
                        self.canvas.draw()

                    except:
                        print(inspect.stack()[0][3])
                        print (sys.exc_info()[0])
                        print (sys.exc_info()[1])
                        print (sys.exc_info()[2])
                        
                    
            else:
                msg = "INSUFFICIENT DATA FOR MEANINGFUL ANSWER."
                messagebox.showinfo(self.engine.title,msg )
        else:
            msg = "No batch selected."
            messagebox.showwarning(self.engine.title,msg)
         

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

    def on_quick_data_analysis(self,):

        self.master.config(cursor="watch")

        self.engine.quick_data_analysis()

        self.master.config(cursor="")

    def on_export(self):

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

        limit = int(self.spElements.get())
        rs = self.engine.read(True, sql, ())

        if rs:
            self.engine.get_xls(limit,rs)
        else:
            msg = "No record data to compute."
            messagebox.showwarning(self.engine.title,msg)
            
    def on_elements(self,):

        f = frames.elements.Dialog(self,self.engine)
        f.on_open()
        
    def on_tests(self,):
        
        f = frames.tests.Dialog(self,self.engine)
        f.on_open()

    def on_units(self,):
        
        f = frames.units.Dialog(self,self.engine)
        f.on_open()           

    def batchs(self,):
        
        f = frames.batchs.Dialog(self,self.engine)
        f.on_open()        

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
    imgicon = PhotoImage(file=os.path.join('icons', 'app.png'))
    root.call('wm', 'iconphoto', root._w, '-default', imgicon)
    #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    #root.geometry("{0}x{1}+0+0".format(1200, 600))
    root.title(engine.title)
    app = Biovarase(engine)
    app.on_open()
    root.mainloop()
  
if __name__ == '__main__':
    main()
