# Biovarase
A clinical quality control data management project

Biovarase is an application to manage clinical quality control data. 
The purpose of Quality Control Assurance in a clinical laboratory is to allow the control of the performances of an analytical procedure showing an alarm as soon as the trial doesn't result in degree to respect the defined analytical rules. 
Biovarase furthermore calculates the classical statistical parameters for the quality control assurance ,e.g. sd, cv%, avg, and even the Imp(%), Bias(%) and TEa (total allowable error) using data retrived from: Current databases on biologic variation: pros, cons and progress Scand J Clin Lab Invest 1999;59:491-500. updated with the most recent specifications made available in 2014. 
It use even the famous Westgard's rules to monitor results dataset. 
All the data are managed by SQLite database and matplotlib. 
To show levey jennings graph, in the main windows select a tests and coiche a relative batch.
To insert, update or delete a batch or a result open from File/Batchs and results.
To export data on a temp excel file click on File/Export.

 Releasing on "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"

To start with Biovarase execute biovarase.py, something like
bc@hal9000:~/biovarase$ python3 biovarase.py
or
bc@hal9000:~/biovarase$ ./biovarase.py
if you previously have done
bc@hal9000:~/biovarase$ chmod +x biochemiae.py
to make biochemiae.py executable

Regards.

change log
2018-02-19
Porting the project to python 3.5, Debian 9 version
Fix redrew problem, now the graph dosen't disappear
Heavy refactoring of the all code
Developed in Python 3.5.3 on Debian Stretch, winter 2018.

2017-05-07
Put graph in the main window.
Struggled to redrew graph but now it's work.
Developed in Python 2.7.9 on Debian Jessie, spring 2017.
TOFIX:
If you make double click on a result, the graph disappear....

![alt tag](https://cloud.githubusercontent.com/assets/5463566/25782001/23d8e1d2-3342-11e7-8fd3-517f6f628288.png)
