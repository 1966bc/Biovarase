# Biovarase
## A clinical quality control data management project

Biovarase is an application to manage clinical quality control data.

The purpose of Quality Control Assurance in a clinical laboratory is to allow the control of the performances of an analytical procedure showing an alarm as soon as the trial doesn't result in the degree to respect the defined analytical rules. Biovarase furthermore calculates the classical statistical parameters for the quality control assurance ,e.g. sd, cv%, avg, and even the Imp(%), Bias(%) and TEa (total allowable error) using data retrived from: Current databases on biologic variation: pros, cons and progress Scand J Clin Lab Invest 1999;59:491-500. updated with the most recent specifications made available in 2014.
It uses even the famous Westgard's rules to monitor results dataset.
All the data are managed by SQLite database and matplotlib.
To show levey jennings graph, in the main windows select a test and choose the relative batch.
To deactivate/activate a result make double click on it.
To insert, update or delete a batch or a result open from File/Batchs and results.
To export data to a temp excel file click on File/Export.

Biovarase requires Python 3
Biovarase use Tkinter and matplotlib 

 Releasing on "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"

To start with Biovarase execute biovarase.py, something like
bc@hal9000:~/biovarase$ python3 biovarase.py

Regards.

######change log

**2018-11-18**

change format to align text in the listbox, remember to use a font such font='TkFixedFont'
align date and result on graph, did anyone notice this?

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

![alt tag](https://user-images.githubusercontent.com/5463566/48675490-c97f9b00-eb59-11e8-975a-1b2b17aebf9c.png)
