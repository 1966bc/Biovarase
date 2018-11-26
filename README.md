# Biovarase
## A clinical quality control data management project

![alt tag](https://user-images.githubusercontent.com/5463566/48971927-ec5df380-f020-11e8-89d4-ba6294c88a9f.png)

Biovarase is an application to manage clinical quality control data.

The purpose of Quality Control Assurance in a clinical laboratory is to allow the control of the performances of an analytical procedure showing an alarm as soon as the trial doesn't result in the degree to respect the defined analytical rules. Biovarase furthermore calculates the classical statistical parameters for the quality control assurance ,e.g. sd, cv%, avg, and even the Imp(%), Bias(%) and TEa (total allowable error) using data retrived from: Current databases on biologic variation: pros, cons and progress Scand J Clin Lab Invest 1999;59:491-500. updated with the most recent specifications made available in 2014.
It uses even the famous Westgard's rules to monitor results dataset.
All the data are managed by SQLite database and matplotlib.

- To show levey jennings graph, in the main windows select a test and choose the relative batch.
- To update a batch in the main window make right click on it.
- To deactivate/activate a result make double click on it.
- To insert, update or delete a test open from File/Tests.
- To manage batchs and relative results open from File/Data.
- To export data to a temp excel file click on File/Export.
- To export last values in a temp excel file click on Quick Data Analysis

Biovarase requires 

- Python =>3.5
- tkinter
- matplotlib 
- xlwt

Releasing on 
> "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"

To start with Biovarase execute biovarase.py, something like

> bc@hal9000:~/biovarase$ python3 biovarase.py

Regards.


...
## changelog

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

