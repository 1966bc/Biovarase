# Biovarase
## changelog

**2021-03-18**

Changed the way to pass the engine.py class to the whole app.

Now we make.

```python

class App(tk.Tk):
    """Biovarase Main Application start here"""
    def __init__(self):
        super().__init__()

        self.engine = Engine()
        
```

and so we can call it so

```python

self.nametowidget(".").engine.get_frame(self, 8)

last_id = self.nametowidget(".").engine.write(sql, args)
        
```

and so on, this because self.nametowidget(".") returns the actual widget whose path name is "."  and "." is the root.



**2019-12-13**

Add Youden chart.

Youden charts are used to compares two levels of controls and can help to differentiate between systematic and random error.

To know the whole story go here:

[Bio-Rad Blackboard - Youden Charts](https://www.youtube.com/watch?v=XUsMMjjL5eA)



To show a Youden chart select first a test, after select at least two batches and on main menu select File/Youden, 

if the number of results are the same the program will show the plot.


![alt tag](https://user-images.githubusercontent.com/5463566/70846762-e077e600-1e5c-11ea-8fec-627182b73fb2.png)




**2019-11-18**

Add to main frame the expiration date for selected batch.

If the expiration date is less than the current date it will color the row as red ,if 15 days is missing it will color yellow.

In the database the expiration date field of the batches is datetime, but python return it as a string so we have to do this to compare the two dates.

```python

def get_expiration_date(self, expiration_date):
        return (datetime.datetime.strptime(expiration_date, "%d-%m-%Y").date() - datetime.date.today()).days

```
Update in the database years of batches and results with this statements:

```
UPDATE  batches SET expiration =  datetime(expiration, '+6 years')
UPDATE  results SET recived =  datetime(recived, '+4 years')
```

**2019-09-18**

add fix in tools.py because with Python 3.7.3  and Tk '8.6.9' the color in treview doesn't work

[Treeview: wrong color change](https://bugs.python.org/issue36468)


#### Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.


**2019-09-17**

could have missed the unittest?!?!?

Add a folder named test, to launch unittest do somenthing

```
bc@hal9000:~/Biovarase-master/test$ python3 -m unittest
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

this will run all the test named test*. py

all tests are still at a primordial stage but this is the right way.

**2019-09-16**

Delete Biovarase icon file, from now on we will load icon as a base 64 data.

In the engine file we write  base 64 data of the incon file


```python
def get_icon(self):
        return """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAAXNSR0IArs4c
                  6QAAAPBQTFRFAAAAAGbMas7///8A3/3/qeM7AFrH+v//AF/HAJn//v//ndgA
                  AJgAhJGdipaii5ejhZKeACelwOoSZs0wACmlKC41Y8wwKS81p9s6ACykACSl
                  LasAACmhJKcAdMgA3v3/NbcAa8QAyeoA1PYAAFzJACSk9/wAs+8UEJ8AXMYA
                  ruYA//+bZs0yTLcA2/A6AF/JAGDW//94JSoy////IikyjNgmYGt0m9cF4f//
                  gtUABJsA//9b//9NfN0y5PRgACaiACalX2lzQbMA//7//f8AP7IAACql2/QM
                  Xb8A//+p6P//yOoAAGLWFKkAACWl8fqIerPNswAAAAF0Uk5TAEDm2GYAAAABY
                  ktHRACIBR1IAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3AgREA0rdM
                  kpsgAAAJBJREFUGNNVytUSwjAURdHcpKXQUsHd3d3dHf7/b4CZQHPP215zCPn
                  OsHTdMog9U1UU1RRgE+h3Q0MBSPtK72KT/Ji2EDhS1IlBwgBSj7oAwQ4BXGqd
                  OWO2gPxahrfTP0BQnjVH55j7J+DzspuWOZQ5QH1wKma1ZCPBL7Ao7VmuOqmkH
                  /wSXxWiz7XHf4x84g33ag0Bx8dLigAAAABJRU5ErkJggg=="""

```

and in the main file...

```python
def set_icon(self):
        icon = tk.PhotoImage(data=self.engine.get_icon())
        self.call('wm', 'iconphoto', self._w, '-default', icon)   

```

and remember to delete icon from kwars....;)

```python
kwargs={"style":"clam", "title":"Biovarase", "engine":Engine(*args)}

```

if you like you can use this link to convert your file

[Base64.Guru](https://base64.guru/converter/encode/image/gif)


**2019-08-25**

Hello everybody,

here  new items of the project:

- Possibility to set the value of ddof used to calculate the standard deviation with munpy, see check box on the left of the 

statusbar and clicking on it see what happends to sd value. See below link for more info.

[numpy std reference](https://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html)


- Possibility to set the value of Z Score value.  

You can see the Z Score set on the left side of the statusbar, if you want  change it go to main mane, Edit/Set Z Score, open 

the window and change it, if you don't remember the Z Score legal value go to main menu on File/Z Score.


![alt tag](https://user-images.githubusercontent.com/5463566/63646648-60473c80-c716-11e9-9d5e-72b17ff18198.png)



- Possibility to show error bar , show check box on the left of the statusbar and see what happends

- Total refactoring of Tea Plot windows, before the system calculation it'was wrong, now we compute upper and lower limit use 

total error allowable funcion plus 4% as recommended by Biorad on this very interesting video.

[Biological Variation Part 9](https://www.youtube.com/watch?v=b7R2tJWWrvM&list=PL8260BF796E272C8A&index=9)

- Rearrangement of the main menu.


**2019-05-26**

Hello everybody, after having separated all qc funcions in a new module 

named qc.py it’s time to implement a new feature  **Sigma**.

You can see this new wonderful feature launch the analytical goal from

File/Export/Analitycal Goals

I've add even the compute of delta sistematic critical error.

```python

def get_sigma(self, cvw, cvb, target, series):
        """Compute sigma."""
        
        avg = self.get_mean(series)
        tea = self.get_tea(cvw, cvb)
        bias = self.get_bias(avg, target)
        cv = self.get_cv(series)
        sigma = (tea - bias)/cv
        
        return round(sigma,2)
```    

tea is Total Error Allowable.

        
**2019-05-21**

Hello everybody, in this new update you will find a new type of plot, named  **Total Error Plot**

![alt tag](https://user-images.githubusercontent.com/5463566/63646848-68ed4200-c719-11e9-99c2-f0bbc7a8e589.png)


You can launch this plot, after selecting a test,clicking on menu File/Te voice.

For more information you can see this video

[Biological Variation Part 9](https://www.youtube.com/watch?v=b7R2tJWWrvM&list=PL8260BF796E272C8A&index=9)

on Biorad QC youtube chanel video.

By the way all videos are very interesting.

Add in the main window the TE% value, it's compute on engine.py module with this two funcions.

```python

    def get_bias(self, avg, target):
        try:
            bias = abs(round(float((avg-target)/float(target))*100,2))
        except ZeroDivisionError:
            bias = None
        return bias

    def get_et(self, target, avg, cv):

        bias = self.get_bias(avg, target)

        return round(bias + (1.65*cv),2)



```

Minor refactoring on bias compute.


**2019-04-28**

Hello everybody, I've update the main.py module of Biovarase.

Now we pass a number of arbitrary args or kwargs to the main class when we launch main.py script. 

Notice that we pass some default attributes and the Engine class as dictionary and even sys.argv as tuple for future need:




>args = []
    
>for i in sys.argv:
>    args.append(i)
    
>kwargs={"style":"clam", "icon":"biovarase.png", "title":"Biovarase", "engine":Engine()}    




```python

class App(tk.Tk):
    """Biovarase Main Application start here"""
    def __init__(self, *args, **kwargs):
        super(App, self).__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.engine = kwargs['engine']
        self.set_title(kwargs['title'])
        self.set_icon(kwargs['icon'])
        self.set_style(kwargs['style'])
       
        frame = Biovarase(self, *args, **kwargs)
        frame.on_open()
        frame.pack(fill=tk.BOTH, expand=1)

    def set_title(self, title):
        s = "{0} {1}".format(title,  __version__)
        self.title(s)        

    def set_style(self, style):
        self.style = ttk.Style()
        self.style.theme_use(style)        
        self.style.configure('.', background=self.engine.get_rgb(240,240,237))

    def set_icon(self, icon):
        imgicon = tk.PhotoImage(file=icon)
        self.call('wm', 'iconphoto', self._w, '-default', imgicon)        

    def on_exit(self):
        """Close all"""
        if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
            self.engine.con.close()
            self.quit()        

def main():

    args = []
    
    for i in sys.argv:
        args.append(i)
    
    kwargs={"style":"clam", "icon":"biovarase.png", "title":"Biovarase", "engine":Engine()}

    app = App(*args, **kwargs)

    app.mainloop()
    
if __name__ == '__main__':
    main()

```


**2019-03-14**

Hello everybody, after having taken inspiration from this book

[Python GUI programming with Tkinter](https://www.packtpub.com/application-development/python-gui-programming-tkinter)

of Alan D. Moore, that I am intensely studying, I've changed the way to setting up the application.

Now we inherit from the class Tk instead of Frame.

```python
class App(tk.Tk):
    """Biovarase Main Application"""

    def __init__(self):
        super().__init__()

        self.engine = Engine()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
            
        self.set_title()
        self.set_icon()
        self.set_style()
       
        frame = Biovarase(self, engine=self.engine)
        frame.on_open()
        frame.pack(fill=tk.BOTH, expand=1)

```

that call...

```python

class Biovarase(ttk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__()

        self.parent = parent
        self.engine = kwargs['engine']


```

notice that I've change 

```python
self.master.protocol("WM_DELETE_WINDOW",self.on_exit)

```

with

```python
self.protocol("WM_DELETE_WINDOW",self.on_exit)

```
Minor refatcoring:

- keep out elements spinbox from main frame
- add Elements toplevel to manage element numbers to compute data
- the Elements toplevel can be call from main menu, it's a file voices 
- the elements number are write/read on the elements file on main directory and show on status bar text


The book is very cool , thank you alan, now I think that Tkinter can constructively be compare with other tools as wxPython or Qt.


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

