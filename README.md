# Biovarase
A clinical quality control data management project

https://github.com/1966bc/Biovarase/blob/master/biovarase.png

Biovarase is an application to manage clinical quality control data. 
This is the Tkinter version.
The purpose of Quality Control Assurance in a clinical laboratory is to allow the control of the performances of an analytical procedure showing an alarm as soon as the trial doesn't result in degree to respect the defined analytical rules. 
Biovarase furthermore calculates the classical statistical parameters for the quality control assurance ,e.g. sd, cv%, avg, and even the Imp(%), Bias(%) and TEa (total allowable error) using data retrived from: Current databases on biologic variation: pros, cons and progress Scand J Clin Lab Invest 1999;59:491-500. updated with the most recent specifications made available in 2014. 
It use even the famous Westgard's rules to monitor results dataset. 
All the data are managed by SQLite database and matplotlib. 
To show levey jennings graph, in the main windows select a tests and coiche a relative batch.
To insert, update or delete a batch or a result open from File/Batchs and results.
To export data on a temp excel file click on File/Export.

 
 Releasing on "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"

To start with Biovarase execute biovarase.py, something like
bc@hal9000:~/code/tkinter/biovarase$ python biovarase.py

Developed in Python 2.7.9 on Debian Jessie, spring 2017.
Regards.

change log
2017-05-07
Put graph in the main window.
Struggled to redrew graph but now it's work.
TOFIX:
If you make double click on a result, the graph disappear....



