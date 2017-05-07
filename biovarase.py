#!/usr/bin/env python
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   04/05/2017
# version:  0.2                                                                  
#-----------------------------------------------------------------------------

from Tkinter import *
import tkMessageBox
import tkFont
import ttk
import datetime
import threading
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from engine import Engine
import elements, tests, data_manager, units


class Launcher(threading.Thread,):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.engine = Engine()
        self.path = path
    def run(self):
        self.engine.open_file(self.path)


class Biovarase(Frame):
    def __init__(self, master=None):
                
        Frame.__init__(self,master)

        #self.master.resizable(0,0)
        self.engine = Engine()
        self.master.title(self.engine.title)

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

        
        self.format_frame_labels = tkFont.Font(family='Arial',weight='bold')
        self.format_label = tkFont.Font(family='Helvetica',size=14,)
       
             
        self.init_menu()
        self.init_status_bar()
        self.init_window()
     
    def init_menu(self):

        mnuMain = Menu(self.master, bd = 1)
        
        mFile = Menu(mnuMain, tearoff=0, bd = 1)
        mParameters = Menu(mnuMain, tearoff=0, bd = 1)
        mAbout = Menu(mnuMain, tearoff=0, bd = 1)
        
        mnuMain.add_cascade(label="File", menu=mFile)
        mnuMain.add_cascade(label="Info", menu=mAbout)

        mFile.add_command(label="Reset", command=self.on_reset)
        mFile.add_command(label="Export", command=self.on_export)
        mFile.add_command(label="Set Elements", command=self.on_elements)
        mFile.add_command(label="Tests", command=self.on_tests)
        mFile.add_command(label="Batchs and Results", command=self.on_data_manager)
        mFile.add_command(label="Units", command=self.on_units)
        mFile.add_command(label="Exit", command=self.on_exit)
        mAbout.add_command(label="About", command=self.on_about)
     
        self.master.config(menu=mnuMain)

    def init_status_bar(self):

        self.status = Label(self.master, text = self.engine.title, bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)
        
    def init_window(self):

    
        self.pack(fill=BOTH, expand=1,)

        #-----------------------------------------------------------------------
        p0 = Frame(self,bd=5)

        cb_tests = LabelFrame(p0,font=self.format_frame_labels, text='Tests')

        self.cbTests =  ttk.Combobox(cb_tests)
        self.cbTests.bind("<<ComboboxSelected>>", self.on_selected_test)
        self.cbTests.pack(side=TOP,fill=X,expand=0)

        lst_batchs = LabelFrame(p0,font=self.format_frame_labels,text='Batchs')
        
        self.sb_batchs = Scrollbar(lst_batchs,orient=VERTICAL)
        self.lstBatchs = Listbox(lst_batchs,
                                 selectmode=BROWSE,
                                 yscrollcommand=self.sb_batchs.set,
                                 bg='white',)
        self.lstBatchs.config(width=8)
        self.lstBatchs.bind("<<ListboxSelect>>", self.on_selected_batch)
        self.sb_batchs.config(command=self.lstBatchs.yview)

        self.lstBatchs.pack(side=LEFT,fill=BOTH,expand=1)
        self.sb_batchs.pack(fill=Y,expand=1)

        lst_results = LabelFrame(p0,font=self.format_frame_labels,text='Results')
        
        self.sb_results = Scrollbar(lst_results,orient=VERTICAL)
        self.lstResults = Listbox(lst_results,
                                  selectmode=BROWSE,
                                  yscrollcommand=self.sb_results.set,
                                  bg='white',)
        self.lstResults.bind("<<ListboxSelect>>", self.on_selected_result)
        self.lstResults.bind('<Double-Button-1>', self.on_enable_result)
        self.sb_results.config(command=self.lstResults.yview)

        self.lstResults.pack(side=LEFT,fill=BOTH,expand=1)
        self.engine.ToolTip(self.lstResults, follow_mouse=1, text="Double click to enable-disable current record.")
        self.sb_results.pack(fill=Y,expand=1)

        cb_tests.pack(side=TOP,fill=X, expand=0)
        lst_batchs.pack(side=TOP,fill=BOTH, expand=0)
        lst_results.pack(side=TOP,fill=BOTH, expand=1)
        p0.pack(side=LEFT, fill=Y, expand=0)


        #-----------------------------------------------------------------------
        p1 = Frame(self,bd=5)
        batch_data = LabelFrame(p1,font = self.format_frame_labels, foreground="green",text='Selected batch data')
        st_target = Label(batch_data, text="Target",)
        st_target.pack(fill=X, padx=2, pady=2)
        self.txTarget = Label(batch_data, bg='white',font = self.format_label,foreground="blue", textvariable = self.target)
        self.txTarget.pack(fill=X, padx=2,pady=2)

        st_sd = Label(batch_data, text="Standard Deviation", )
        st_sd.pack(fill=Y, padx=2, pady=2)
        self.txtBatchSD = Label(batch_data, bg='white', font = self.format_label,foreground="orange", textvariable = self.sd)
        self.txtBatchSD.pack(fill=X, padx=2,pady=2)

        st_expiration = Label(batch_data, text="Expiration", )
        st_expiration.pack(fill=Y, padx=2, pady=2)
        self.txtExpiration = Label(batch_data, bg='white',font = self.format_label, textvariable = self.expiration)
        self.txtExpiration.pack(fill=X, padx=2,pady=2)

        elements = Label(batch_data, text="Elements", )
        elements.pack(fill=X, expand=0)
        self.spElements = Spinbox(batch_data,bg='white',font = self.format_label, from_=1, to=365,justify=CENTER,width=3,wrap=True,insertwidth=1, textvariable=self.elements)
        self.spElements.pack(fill=X, expand=0)

        calculated_data = LabelFrame(p1, font = self.format_frame_labels, foreground="green",text='Calculated data')
     
        st_avg = Label(calculated_data, text="Average", )
        st_avg.pack(fill=X, padx=2, pady=2)
        self.txAverage = Label(calculated_data,  bg='white',font = self.format_label,foreground="blue", textvariable = self.average)
        self.txAverage.pack(fill=X, padx=2,pady=2)

        st_sd = Label(calculated_data, text="Standard Deviation", )
        st_sd.pack(fill=X, padx=2, pady=2)
        self.txtSD = Label(calculated_data,  bg='white',font = self.format_label,foreground="orange", textvariable = self.calculated_sd)
        self.txtSD.pack(fill=X, padx=2,pady=2)

        st_cv = Label(calculated_data, text="CV%",)
        st_cv.pack(fill=X, padx=2, pady=2)
        self.txCV = Label(calculated_data, bg='white',font = self.format_label, textvariable = self.calculated_cv)
        self.txCV.pack(fill=X, padx=2,pady=2)

        st_bias = Label(calculated_data, text="Bias", )
        st_bias.pack(fill=X, padx=2, pady=2)
        self.txBias = Label(calculated_data,  bg='white',font = self.format_label, textvariable = self.bias)
        self.txBias.pack(fill=X, padx=2,pady=2)

        st_westgard = Label(calculated_data, text="Westgard",)
        st_westgard.pack(fill=X, padx=2, pady=2)
        self.txWestgard = Label(calculated_data,  bg='white',font = self.format_label, textvariable = self.westgard)
        self.txWestgard.pack(fill=X, padx=2,pady=2)

        st_range = Label(calculated_data, text="Range",)
        st_range.pack(fill=X, padx=2, pady=2)
        self.txRange = Label(calculated_data, bg='white',font = self.format_label, textvariable = self.range)
        self.txRange.pack(fill=X, padx=2,pady=2)

        batch_data.pack(side=TOP,fill=X, expand=0)
        calculated_data.pack(side=TOP,fill=X, expand=0)
        p1.pack(side=LEFT, fill=Y, expand=0)
 
        self.frame_plot = Frame(self,bd=5)
       
        self.frame_plot.pack(side=RIGHT, fill=BOTH, expand=1,padx=5, pady=5)
     
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
                self.lj.get_tk_widget().delete("all")
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

    #TOFIX: when enale-disable the graph doesn't redew
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
                        dates.append(datetime.datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S'))

                    
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

                    
            else:
                msg = "INSUFFICIENT DATA FOR MEANINGFUL ANSWER."
                messagebox.showinfo(self.engine.title,msg )
        else:
            msg = "No batch selected."
            tkMessageBox.showwarning(self.engine.title,msg)

    def draw(self, levey_jennings, axes):

        self.reset_graph()

        self.levey_jennings = levey_jennings
    
        self.axes = axes
            
        self.lj = FigureCanvasTkAgg(levey_jennings, self.frame_plot)
        self.lj.show()
        self.lj.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
        self.lj_toolbar = NavigationToolbar2TkAgg(self.lj, self.frame_plot)
        self.lj_toolbar.update()
        #enable for keep on bottom
        #self.lj._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)    
  

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
        path = tempfile.mktemp (".xls")
        limit = int(self.spElements.get())
        obj = self.engine.get_xls(limit,rs)
        obj.save(path)
        Launcher(path).start()    

    def on_elements(self,):

        obj = elements.Dialog(self,self.engine)
        obj.attributes("-topmost", True)
        obj.on_open()
        obj.wait_visibility()
        obj.grab_set()
        self.master.wait_window(obj)

    def on_tests(self,):
        
        obj = tests.Dialog(self,self.engine)
        obj.on_open()

    def on_units(self,):
        
        obj = units.Dialog(self,self.engine)
        obj.on_open()           

    def on_data_manager(self,):
        
        obj = data_manager.Dialog(self,self.engine)
        obj.on_open()        
      
    def on_about(self,):
        tkMessageBox.showinfo(self.engine.title, self.engine.about)   
        
    def on_exit(self):
        if tkMessageBox.askokcancel(self.engine.title, "Do you want to quit?"):
            self.master.destroy()
            
if __name__ == "__main__":

    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    #full screen
    root.geometry(str(width) + "x" + str(height))
    app = Biovarase(master=root)
    app.on_open()
    app.master.protocol("WM_DELETE_WINDOW",app.on_exit)
    app.mainloop()
