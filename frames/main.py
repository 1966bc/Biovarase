#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018
# version:  0.1                                                                
#-----------------------------------------------------------------------------
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from engine import Engine

import frames.elements
import frames.tests
import frames.data_manager
import frames.units

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
        self.levey_jennings = None
        self.axes = None
        
        self.init_menu()
        self.init_ui()
        self.init_status_bar()

    def init_menu(self):

        m_main = Menu(self, bd = 1)
        
        m_file = Menu(m_main, tearoff=0, bd = 1)
        m_about = Menu(m_main, tearoff=0, bd = 1)
        
        m_main.add_cascade(label="File", underline=1, menu=m_file)
        m_main.add_cascade(label="?", underline=0, menu=m_about)

        items = (("Reset",self.on_reset),
                 ("Export",self.on_export),
                 ("Elements",self.on_elements),
                 ("Tests",self.on_tests),
                 ("Batch and Results",self.on_data_manager),
                 ("Units",self.on_units),
                 ("Exit",self.on_exit),)

        for i in items:
            m_file.add_command(label=i[0],underline=0, command=i[1])

          
        m_about.add_command(label="About",underline=0, command=self.on_about)
     
        self.master.config(menu=m_main)        
        
    def init_ui(self):

        self.pack(fill=BOTH, expand=1,)

        #-----------------------------------------------------------------------
        p0 = Frame(self,bd=5)

        cb_tests = LabelFrame(p0, text='Tests')

        self.cbTests =  ttk.Combobox(cb_tests)
        self.cbTests.bind("<<ComboboxSelected>>", self.on_selected_test)
        self.cbTests.pack(side=TOP,fill=X,expand=0)

        lst_batchs = LabelFrame(p0,text='Batchs')

        self.lstBatchs = self.engine.get_listbox(lst_batchs,)
        self.lstBatchs.bind("<<ListboxSelect>>", self.on_selected_batch)
       
        lst_results = LabelFrame(p0,text='Results')

        self.lstResults = self.engine.get_listbox(lst_results,)
        self.lstResults.bind("<<ListboxSelect>>", self.on_selected_result)
        self.lstResults.bind('<Double-Button-1>', self.on_enable_result)
        
        cb_tests.pack(side=TOP,fill=X, expand=0)
        lst_batchs.pack(side=TOP,fill=BOTH, expand=0)
        lst_results.pack(side=TOP,fill=BOTH, expand=1)
        p0.pack(side=LEFT, fill=Y, expand=0)


        #-----------------------------------------------------------------------
        p1 = Frame(self,bd=5)
        w = LabelFrame(p1, foreground="green",text='Selected batch data')

        lbl = Label(w, text="Target")
        lbl.pack()
        
        self.txTarget = Label(w, bg='white',foreground="blue", textvariable = self.target)
        self.txTarget.pack(fill=X, padx=2,pady=2)

        lbl = Label(w, text="Standard Deviation")
        lbl.pack()

        self.txtBatchSD = Label(w, bg='white', foreground="orange", textvariable = self.sd)
        self.txtBatchSD.pack(fill=X, padx=2,pady=2)

        lbl = Label(w, text="Expiration")
        lbl.pack()
        
        self.txtExpiration = Label(w, bg='white', textvariable = self.expiration)
        self.txtExpiration.pack(fill=X, padx=2,pady=2)

        lbl = Label(w, text="Elements")
        lbl.pack()

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

        w.pack(side=TOP,fill=X, expand=0)

        w = LabelFrame(p1, foreground="green",text='Calculated data')
     
        lbl = Label(w, text="Average")
        lbl.pack()
        
        self.txAverage = Label(w,  bg='white',foreground="blue", textvariable = self.average)
        self.txAverage.pack(fill=X, padx=2,pady=2)

        lbl = Label(w, text="Standard Deviation")
        lbl.pack()

        self.txtSD = Label(w,  bg='white',foreground="orange", textvariable = self.calculated_sd)
        self.txtSD.pack(fill=X, padx=2,pady=2)

        lbl = Label(w, text="CV%")
        lbl.pack()
                
        self.txCV = Label(w, bg='white', textvariable = self.calculated_cv)
        self.txCV.pack(fill=X, padx=2,pady=2)

        lbl = Label(w, text="Bias")
        lbl.pack()

        self.txBias = Label(w,  bg='white', textvariable = self.bias)
        self.txBias.pack(fill=X, padx=2,pady=2)

        lbl = Label(w, text="Westgard")
        lbl.pack()

        self.txWestgard = Label(w,  bg='white', textvariable = self.westgard)
        self.txWestgard.pack(fill=X, padx=2,pady=2)

        lbl = Label(w, text="Range")
        lbl.pack()

        self.txRange = Label(w, bg='white', textvariable = self.range)
        self.txRange.pack(fill=X, padx=2,pady=2)

        w.pack(side=TOP,fill=X, expand=0)

        p1.pack(side=LEFT, fill=Y, expand=0)
 
        self.frame_plot = Frame(self,bd=5)
       
        self.frame_plot.pack(side=RIGHT, fill=BOTH, expand=1,padx=5, pady=5)

    def init_status_bar(self):
        
        self.status = Label(self.master, text = self.engine.title, bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)        

    def on_open(self):
        self.set_elements()
        self.on_reset()

    def set_elements(self):
        elements = self.engine.get_parameters()
        self.elements.set(elements['elements'])
        
    def on_reset(self):

        self.rs = None
        self.selected_batch = None
        self.lstBatchs.delete(0, END)
        self.lstResults.delete(0, END)

        index = 0
        self.dict_tests={}
        l = []
       

        sql = "SELECT tests.test_id,tests.test||' '||samples.sample\
               FROM tests\
               INNER JOIN samples ON tests.sample_id = samples.sample_id\
               WHERE tests.enable=1\
               ORDER BY tests.test"
        
        rs = self.engine.read(True, sql, ())

        for i in rs:
            self.dict_tests[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbTests['values']=l        
        
        self.reset_texts()
        self.reset_graph()

    def reset_graph(self):

        if self.levey_jennings is not None:
            try:
                self.levey_jennings.clf()
                self.lj_graph.get_tk_widget().delete("all")
                self.axes.clear()
                for child in self.frame_plot.winfo_children():
                    child.destroy()
            except:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])

    def reset_texts(self):

        self.expiration.set(None)
        self.target.set(0)
        self.sd.set(0)
        self.average.set(0)
        self.bias.set(0)
        self.westgard.set('Accept')
        self.calculated_sd.set(0)
        self.calculated_cv.set(0)
        self.range.set(0)
        

    def on_selected_test(self,event):

        index = self.cbTests.current()
        test_id = self.dict_tests[index]
        self.selected_test = self.engine.get_selected('tests','test_id', test_id)

       
        self.lstBatchs.delete(0, END)
        self.lstResults.delete(0, END)
        self.reset_texts()

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
    
    def on_selected_batch(self,event):

        if self.lstBatchs.curselection():

            index = self.lstBatchs.curselection()[0]
            pk = self.dict_batchs.get(index)
            self.selected_batch = self.engine.get_selected('batchs','batch_id', pk)

            self.set_batch_values()
            self.set_results_values()
            

    def set_batch_values(self):

        self.expiration.set(self.selected_batch[3])
        self.target.set(self.selected_batch[4])
        self.sd.set(self.selected_batch[5])            

    def set_results_values(self,):           
            
            self.lstResults.delete(0, END)

            index = 0
            self.dict_results={}
            series = []

            sql = "SELECT * FROM lst_results WHERE batch_id = ? LIMIT ?"
            rs = self.engine.read(True, sql, (self.selected_batch[0],int(self.spElements.get())))

            target = float(self.selected_batch[4])
            sd = float(self.selected_batch[5])

            if rs:

                for i in rs:

                    s = '{}{:>10}'.format(i[2],i[1])
                    self.lstResults.insert(END, s)

                    result = float(i[1])
                    is_enabled = i[3]
        
                    self.set_results_row_color(index, result, is_enabled, target, sd)
                    
                    self.dict_results[index]=i[0]
                    series.append(i[1])
                    index+=1

                avg = round(np.mean(series),2)
                sd = round(np.std(series),2)
                self.average.set(avg)
                self.bias.set(round((avg-target)/(target)*100,2))
                self.set_westgard(series)
                self.calculated_sd.set(sd)
                self.calculated_cv.set(round((sd/avg)*100,2))
                self.range.set(round(np.ptp(series),2))

                self.on_plot()
                     
    def set_results_row_color(self, index, result, is_enabled, target, sd):

        if is_enabled == 0:
            self.lstResults.itemconfig(index, {'bg':'light gray'})
        else:
            if result > target:
                #result > 3sd
                if result > (target + (sd*3)):
                    self.lstResults.itemconfig(index, {'bg':'red'})
                #if result is > 2sd and < +3sd
                elif (target + (sd*2) <= result <= target + (sd*3)):
                    self.lstResults.itemconfig(index, {'bg':'yellow'})

            elif result < target:
                #result < 3sd
                if result < (target - (sd*3)):
                    self.lstResults.itemconfig(index, {'bg':'red'})
                    #if result is > -2sd and < -3sd
                elif (target - (sd*2) <= result <= target - (sd*3)):
                    self.lstResults.itemconfig(index, {'bg':'yellow'})
               
    def set_westgard(self,series):

        if len(series) > 9:
            rule = self.engine.get_violation(self.selected_batch[4],self.selected_batch[5],series)
        else:
            rule = "No data"
        
        self.westgard.set(rule)
        
    def on_selected_result(self,event):

        if self.lstResults.curselection():
            
            index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(index)
            self.selected_result = self.engine.get_selected('results','result_id', pk)

    #TOFIX: when enale-disable the graph doesn't redrew
    def on_enable_result(self, event):

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
            self.set_results_values()
            
            #self.on_selected_batch(self.lstBatchs)
            
                
    def get_um(self,):

        sql = "SELECT unit FROM units WHERE unit_id =?"
        return self.engine.read(False, sql, (self.selected_test[2],))


    def on_plot(self):

        self.reset_graph()

        if self.selected_batch is not None :

            sql = "SELECT result_id,\
                          ROUND(result,2) AS result,\
                          strftime('%d', recived),\
                          recived,\
                          enable\
                   FROM results\
                   WHERE batch_id = ?\
                   ORDER BY recived DESC\
                   LIMIT ?"

            rs = self.engine.read(True, sql, (self.selected_batch[0],int(self.spElements.get())))

            all_data = len(rs)
            #compute record with enable = 1
            rs = tuple(i for i in rs if i[4]!=0)
            compute_data = len(rs)

            if rs is not None:

                if compute_data<3:
                    msg = ("%s : lot %s INSUFFICIENT DATA FOR MEANINGFUL ANSWER"% (self.selected_test[3],self.selected_batch[2]))
                else:
                    
                    target = self.selected_batch[4]
                    sd = self.selected_batch[5]
                    data = []
                    dates = []
                    my_xticks = []

                    for i in reversed(rs):
                        #print (i)
                        data.append(i[1])
                        my_xticks.append(i[2])
                        #dates.append(datetime.datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S'))
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
   
                        levey_jennings = plt.figure(self.selected_batch[0])
                        axes = levey_jennings.add_subplot(111)
                        #levey_jennings.subplots_adjust(bottom=0.)
                       
                        axes.set_xticks(range(len(data)), my_xticks)
                        
                        axes.plot(data,marker="8",label='data')
                        for x,y in enumerate(data):
                            axes.text(x, y, str(y),)
                           
                        axes.plot(target_line,label='target', linewidth=2)
                        axes.legend(loc='upper right')
                        axes.plot(sd1line,color="green",label='+1 sd',linestyle='--')
                        axes.plot(sd2line,color="orange",label='+2 sd',linestyle='--')
                        axes.plot(sd3line,color="red",label='+3 sd',linestyle='--')
                        axes.plot(sd1_line,color="green",label='-1 sd',linestyle='--')
                        axes.plot(sd2_line,color="orange",label='-2 sd',linestyle='--')
                        axes.plot(sd3_line,color="red",label='-3 sd',linestyle='--')
                        
                        um = self.get_um()
                        axes.set_ylabel(str(um[0]))
                     
                        msg = "Test: %s Batch: %s Expiration: %s " %(self.selected_test[3],
                                                                     self.selected_batch[2],
                                                                     self.selected_batch[3],)
                        axes.set_title(msg)

                        text_data = (avg,sd,cv,self.format_interval_date(dates), compute_data, all_data)

                        axes.text(0.95, 0.01,
                                 'average:%s sd:%s cv:%s %s computed %s on %s results'%text_data,
                                 verticalalignment='bottom',
                                 horizontalalignment='right',
                                 transform=axes.transAxes,
                                 color='black')

                        self.draw(levey_jennings, axes)

                    except:
                        print (sys.exc_info()[0])
                        print (sys.exc_info()[1])
                        print (sys.exc_info()[2])
                        
                    
            else:
                msg = "INSUFFICIENT DATA FOR MEANINGFUL ANSWER."
                messagebox.showinfo(self.engine.title,msg )
        else:
            msg = "No batch selected."
            tkMessageBox.showwarning(self.engine.title,msg)

    def draw(self, levey_jennings, axes):

        try:
            
            self.levey_jennings = levey_jennings
        
            self.axes = axes
                
            self.lj_graph = FigureCanvasTkAgg(levey_jennings, self.frame_plot)
            self.lj_graph.show()
            self.lj_graph.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
            self.lj_toolbar = NavigationToolbar2TkAgg(self.lj_graph, self.frame_plot)
            self.lj_toolbar.update()
            #enable for keep on bottom
            #self.lj_graph._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        except:
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])            
  

    def format_interval_date(self,dates):

        x = min(dates)
        s1 = "%s-%s-%s" %(x.day,x.month,x.year)
        x = max(dates)
        s2 = "%s-%s-%s" %(x.day,x.month,x.year)
                
        return  "from %s to %s"%(s1,s2)

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

        rs = self.engine.read(True, sql, ())
        limit = int(self.spElements.get())
        self.engine.get_xls(limit,rs)
        
       

    def on_elements(self,):

        f = frames.elements.Dialog(self,self.engine)
        f.on_open()
        
    def on_tests(self,):
        
        f = frames.tests.Dialog(self,self.engine)
        f.on_open()

    def on_units(self,):
        
        f = frames.units.Dialog(self,self.engine)
        f.on_open()           

    def on_data_manager(self,):
        
        f = frames.data_manager.Dialog(self,self.engine)
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
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.title(engine.title)
    app = Biovarase(engine)
    app.on_open()
    root.mainloop()
  
if __name__ == '__main__':
    main()
