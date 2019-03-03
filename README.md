# Biovarase
## A clinical quality control data management project

![alt tag](https://user-images.githubusercontent.com/5463566/52530419-def20480-2d05-11e9-8c57-8376fde0efad.png)

Biovarase is an application to manage clinical quality control data.

The purpose of Quality Control Assurance in a clinical laboratory is to allow the control of the performances of an analytical procedure showing an alarm as soon as the trial doesn't result in the degree to respect the defined analytical rules. Biovarase furthermore calculates the classical statistical parameters for the quality control assurance ,e.g. sd, cv%, avg, and even the Imp(%), Bias(%) and TEa (total allowable error) using data retrived from: Current databases on biologic variation: pros, cons and progress Scand J Clin Lab Invest 1999;59:491-500. updated with the most recent specifications made available in 2014.
It uses even the famous Westgard's rules to monitor results dataset.
All the data are managed by SQLite database and matplotlib.

- To show levey jennings graph, in the main windows select a test and choose the relative batch.
- To manage batches in the main window select a test and on menubar choice Batchs/Add batch or Update batch.
- To manage results in the main window select a batch and on menubar choice Results/Add result or Update result.
- To manage rejections in the main window select a result, in the window that will open add or update rejection type.
- To manage actions in the main window use File/Actions.
- To manage units in the main window use File/Units.
- To insert, update or delete a test use File/Tests.
- To manage batchs and relative results use File/Data.
- To export some xls data choice an item from File/Export

Biovarase requires 

- Python =>3.5
- tkinter
- matplotlib 
- xlwt

Releasing on 
> "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"

To start with Biovarase execute biovarase.py, something like

> bc@hal9000:~/biovarase$ python3 biovarase.py

regards.


...
## changelog

**2019-03-03**

Changed passing arguments mechanism, when build args for update sql statements.

Now we use a tuple instead of a list.

before

```python
#from test.py

def get_values(self,):
        
        return [self.dict_samples[self.cbSamples.current()],
                self.dict_units[self.cbUnits.current()],
                self.test.get(),
                self.cvw.get(),
                self.cvb.get(),
                self.enable.get()]
                
#on on_save callback....

args = self.get_values()

if self.index is not None:
    
    sql = self.engine.get_update_sql('tests', 'test_id')
    #args is a list
    args.append(self.selected_test[0])

```

now

```python


def get_values(self,):
        
        return (self.dict_samples[self.cbSamples.current()],
                self.dict_units[self.cbUnits.current()],
                self.test.get(),
                self.cvw.get(),
                self.cvb.get(),
                self.enable.get())
            
args = self.get_values()

#on on_save callback....

if self.index is not None:
    
    sql = self.engine.get_update_sql('tests', 'test_id')
    #args is a tuple    
    args = (*args, self.selected_test[0])
```



**2019-02-28**

Changed passing arguments mechanism, init method, between all toplevel.

before
```python

#toplevel tests launch function from main.py
def on_tests(self,):
        f = frames.tests.Dialog(self,self.engine)
        f.on_open()

#tests.py init method
class Dialog(tk.Toplevel):     
    def __init__(self, parent, engine):
        super().__init__(name='tests')

        self.parent = parent
        self.engine = engine
```

now
```python

#toplevel tests launch function from main.py
def on_tests(self,):
        f = frames.tests.Dialog(self, engine=self.engine)
        f.on_open()

#tests.py init method
class Dialog(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='tests')
        
        self.parent = parent
        self.engine = kwargs['engine']

```
God bless *args, **kwargs....

go here for stimuli your brain

[skipperkongen](http://skipperkongen.dk/2012/04/27/python-init-multiple-heritance/)


**2019-02-16**

Add to every toplevel this code

```python
self.attributes('-topmost', True)
```

to keep toplevel in front of main window.

change reset function on data.py, set messagebox.askyesno default button on No.

```python
def on_reset_database(self, evt):

        msg = "You are about to delete the entire database.\nAre you sure? "

        if messagebox.askyesno(self.engine.title, msg, default='no', parent=self) == True:

            self.engine.dump_db()
            
            sql = ("DELETE FROM tests",
                   "DELETE FROM batches",
                   "DELETE FROM results",
                   "DELETE FROM rejections",)

            for statement in sql:
                self.engine.write(statement,())
            
            
            self.parent.on_reset()
            self.on_cancel()  
        else:
            messagebox.showinfo(self.engine.title, self.engine.abort, parent=self)              
```



**2019-02-06**

Migrate almost anything from tkinter to ttk.

Improve the field control function in tools.py module, now we check even if the user try to use a value not

present on combobox, before save a record.

```python
def on_fields_control(self, container):

        msg = "Please fill all fields."

        for w in container.winfo_children():
            for field in w.winfo_children():
                if type(field) in(ttk.Entry,ttk.Combobox):
                    if not field.get():
                        messagebox.showwarning(self.title,msg)
                        field.focus()
                        return 0
                    elif type(field)==ttk.Combobox:
                          if field.get() not in field.cget('values'):
                              msg = "You can choice only values in the list."
                              messagebox.showwarning(self.title,msg)
                              field.focus()
                              return 0
```



**2019-01-01**

Hi all and happy new year.

Add a new powerfull toplevel frame.

In the main frame, select a test and after go to menu bar and press File/Plots.

The following window will appear.

![alt tag](https://user-images.githubusercontent.com/5463566/50571419-fdc9b680-0da9-11e9-9404-3f57ece11968.png)

It's cool, not?

The number of graphs are created at run time, look at this code line in plots.py file.

count = len(batches)*100+11

count is subplot args and depend of the numbers of batch data to show. 

regards.




**2018-12-25**

Hi all and merry christmas, this is the new 4.2 version of Biovarase.

I' ve use this powerfull tool, [Spyder](https://www.spyder-ide.org/), to refactoring all the project.

It's very cool;)

Change widgets.py to tools.py because it seems widgets it' s a reserved word in deep python tk file....

Clean, with the Spider help, very much code lines.


**2018-12-09**

Add rejections managements.Now you can add actions, something like "Calibation","Blanck cuvette","Substitutions" in the relative frame and save on the database rejection actions on selected results.

Rewrite all westgard class, now it's better.

Write a better menu bar, with some items groupig, see Export item.

Improve add/update file, now we use index to understand if the frame it's open to update or ti insert an item.

Some minor refactoring

**2018-11-24**

Change the redrew mechanism, now Biovarase doesn't rebuild the graph from scratch when you select a batch, but update only the data.

I've look here [Chapman Siu](https://gist.github.com/1966bc/824372b59c03425d02d816f1f02f8685) to learn how do it.

Add Quick Data Analysis function on the menu to analyze the last dataset for every test and relative bacth.

Add histogram to plot frequency distribution of a dataset.

Some minor refactoring on main.py code.

We deserve an updating to version 2.8. ;)


**2018-11-18**

Change format to align text in the listbox, remember to use a font such font='TkFixedFont'.

Align date and result on graph, did anyone notice this?

**2018-09-23**

Biovarase change is dress....and make minor refactoring.

**2018-08-30**

Change elements data from shelve to sqlite.
Fix some minor bug on test.py

**2018-02-19**

Porting the project to python 3.5, Debian 9 version
Fix redrew problem, now the graph dosen't disappear
Heavy refactoring of the all code
Developed in Python 3.5.3 on Debian Stretch, winter 2018.

**2017-05-07**

Put graph in the main window.
Struggled to redrew graph but now it's work.
Developed in Python 2.7.9 on Debian Jessie, spring 2017.
TOFIX:
If you make double click on a result, the graph disappear....
...

