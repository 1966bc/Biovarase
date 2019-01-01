# Biovarase
## A clinical quality control data management project

![alt tag](https://user-images.githubusercontent.com/5463566/50438017-7b924b80-08ec-11e9-97d1-a965e99ca51b.png)

Biovarase is an application to manage clinical quality control data.

The purpose of Quality Control Assurance in a clinical laboratory is to allow the control of the performances of an analytical procedure showing an alarm as soon as the trial doesn't result in the degree to respect the defined analytical rules. Biovarase furthermore calculates the classical statistical parameters for the quality control assurance ,e.g. sd, cv%, avg, and even the Imp(%), Bias(%) and TEa (total allowable error) using data retrived from: Current databases on biologic variation: pros, cons and progress Scand J Clin Lab Invest 1999;59:491-500. updated with the most recent specifications made available in 2014.
It uses even the famous Westgard's rules to monitor results dataset.
All the data are managed by SQLite database and matplotlib.

- To show levey jennings graph, in the main windows select a test and choose the relative batch.
- To manage batches in the main window select a test and on menubar choice Batchs/Add batch or Update batch.
- To manage results in the main window select a batch and on menubar choice Results/Add result or Update result.
- To manage rejections in the main window select a result, in the toplevel window that will open add or update rejection type.
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

**2019-01-01**

Hi all and happy new year.

Add a new powerfull toplevel frame.

In the main frame, select a test and after go to menu bar on File/Batchs Plots.

The following Toplevel framewill appear.

![alt tag](https://user-images.githubusercontent.com/5463566/50571419-fdc9b680-0da9-11e9-9404-3f57ece11968.png)

It' cool, not?

The number of graphs are created at run time, look at this code line in batch_plots.py file.

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

