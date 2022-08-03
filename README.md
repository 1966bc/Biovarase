[![Python 3](https://img.shields.io/badge/python-3%20-blue.svg)](https://www.python.org/downloads/)
[![Tkinter](https://img.shields.io/badge/Tkinter%20-green.svg)](https://docs.python.org/3/library/tk.html)
[![Matplotlib](https://img.shields.io/badge/Matplotlib%20-red.svg)](https://matplotlib.org/)
[![license](https://img.shields.io/badge/license-GPL%203-orange.svg)](./LICENSE)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

# Biovarase

## A clinical quality control data management project

![alt tag](https://user-images.githubusercontent.com/5463566/69223427-9e1ff980-0b7b-11ea-9699-7a62aa490efa.png)

Biovarase is an application to manage clinical quality control data.

The purpose of Quality Control Assurance in a clinical laboratory is to allow the control of the performances of an analytical procedure showing an alarm as soon as the trial doesn't result in the degree to respect the defined analytical rules. Biovarase furthermore calculates the classical statistical parameters for the quality control assurance ,e.g. sd, cv%, avg, and even the Imp(%), Bias(%) and TEa (total allowable error) using data retrived from: Current databases on biologic variation: pros, cons and progress Scand J Clin Lab Invest 1999;59:491-500. updated with the most recent specifications made available in 2014.
It uses even the famous Westgard's rules to monitor results dataset.
All the data are managed by SQLite database and matplotlib.

- To show levey jennings graph, in the main windows select a test and choose the relative batch.
- To manage batches in the main window select a test and on menubar choice Batchs/Add batch or Update batch.
- To manage results in the main window select first a batch and after a result or on menubar choice Results/Add result or Update result.
- To manage rejections in the main window select a result after check Enable Rejections on statusbar, in the window that will open add or update rejection type.
- To manage actions in the main window use Edit/Actions.
- To manage units in the main window use Edit/Units.
- To insert, update or delete a test use Edit/Tests.
- To manage batchs and relative results use Edit/Data.
- To set the number of elements to compute Edit/Set Elements.
- To set the Z Score use Edit/Set Z Score.
- To export some xls data choice an item from File/Export

Biovarase requires 

- Python =>3.5
- tkinter
- matplotlib 
- xlwt
- numpy

Releasing on 
> "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"

To start with Biovarase execute biovarase.py, on linux after unpucking do something like

> bc@hal9000:~$ cd Biovarase-master/

> bc@hal9000:~/Biovarase-master$ chmod +x biovarase.py

> bc@hal9000:~/Biovarase-master$ ./biovarase.py 

regards.


