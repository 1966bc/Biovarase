[![Python 3](https://img.shields.io/badge/python-3%20-blue.svg)](https://www.python.org/downloads/)
[![Tkinter](https://img.shields.io/badge/Tkinter%20-green.svg)](https://docs.python.org/3/library/tk.html)
[![Matplotlib](https://img.shields.io/badge/Matplotlib%20-red.svg)](https://matplotlib.org/)
[![license](https://img.shields.io/badge/license-GPL%203-orange.svg)](./LICENSE)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

# Biovarase

## A clinical quality control data management project

![alt tag](https://user-images.githubusercontent.com/5463566/283523174-9e9bbafd-f96e-462e-a77f-a7c6cff55c1f.png)

Biovarase is an application to manage clinical quality control data.

The purpose of Quality Control Assurance in a clinical laboratory is to allow the control of the performances of an analytical procedure showing an alarm as soon as the trial doesn't result in the degree to respect the defined analytical rules. Biovarase furthermore calculates the classical statistical parameters for the quality control assurance ,e.g. sd, cv%, avg, and even the Imp(%), Bias(%) and TEa (total allowable error) using data retrived from: Current databases on biologic variation: pros, cons and progress Scand J Clin Lab Invest 1999;59:491-500. updated with the most recent specifications made available in 2014.
It uses even the famous Westgard's rules to monitor results dataset.
All the data are managed by SQLite database and matplotlib.

Take a look at the manual for getting started with Biovarase.

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
>
> To login you can use as user "adm" and password "adm"

![alt tag](https://user-images.githubusercontent.com/5463566/277103748-2a82de97-34ac-459d-afb6-6f4fa4d4afc3.png)

regards.


