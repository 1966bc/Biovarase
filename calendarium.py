#!/usr/bin/env python3
"""Provides a primitive light widget to manage calendar date in tkinter projects.

How import;
from calendarium import Calendarium

How nstantiate in your frame:
self.start_date = Calendarium(self)
self.start_date = Calendarium(self,"Start Date")

How pack:
#f is a tkinter widget such as Frame
if use row and col
self.start_date.get_calendarium(f, row, col)
If use pack()
self.start_date.get_calendarium(f,)

Set today date:
self.start_date.set_today()

Check if a date is right formated:

before you must import this:
from tkinter import messagebox

if self.start_date.get_date()==False:
    msg = "Date format error"
    messagebox.showerror('My Title', msg, parent=self)

Notice that in the spinbox widget we allowed only integers.
Calendarium use datetime.date to set/get date.

"""
import sys
import datetime
from datetime import date
import tkinter as tk


__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "1.0"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-08-26"
__status__ = "Beta"

class Calendarium(tk.Frame):
    def __init__(self,caller, name, *args, **kwargs):
        super().__init__()

        self.args = args
        self.kwargs = kwargs

        self.vcmd = (self.register(self.validate), '%d', '%P', '%S')

        self.caller = caller
        self.name = name
        
        self.day = tk.IntVar()
        self.month =  tk.IntVar()
        self.year =  tk.IntVar()
       
        
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )


    def get_calendarium(self, container, row=None, col=None):
        

        w = tk.LabelFrame(container,
                          text=self.name,
                          borderwidth=1,
                          padx=2,pady=2,
                          relief=tk.GROOVE,)


        day_label = tk.LabelFrame(w, text="Day")

        d = tk.Spinbox(day_label, bg='white', fg='blue',width=2,
                       from_=1, to=31,
                       validate = 'key',
                       validatecommand = self.vcmd,
                       textvariable=self.day,
                       relief=tk.GROOVE,)

        month_label = tk.LabelFrame(w, text="Month")
        m = tk.Spinbox(month_label, bg='white',fg='blue', width=2,
                       from_=1, to=12,
                       validate = 'key',
                       validatecommand = self.vcmd,
                       textvariable=self.month,
                       relief=tk.GROOVE,)

        year_label = tk.LabelFrame(w, text="Year")
        y = tk.Spinbox(year_label, bg='white', fg='blue',width=4,
                       validate = 'key',
                       validatecommand = self.vcmd,
                       from_=1900, to=3000,
                       textvariable=self.year,
                       relief=tk.GROOVE,)

        for p,i in enumerate((day_label,d,month_label,m,year_label,y)):
            if  row is not None:
                i.grid(row=0, column=p, padx=5, pady=5,sticky=tk.W)
            else:
                i.pack(side=tk.LEFT, fill=tk.X, padx=2)
                 
                 
        if row is not None:
            w.grid(row = row, column = col,sticky=tk.W)
        else:
            w.pack()

        return w

    def set_today(self,):

        today = date.today()

        self.day.set(today.day)
        self.month.set(today.month)
        self.year.set(today.year)

    def get_date(self,):

        try:
            return datetime.date(self.year.get(), self.month.get(), self.day.get())
        except ValueError:
            return False

        
    def get_timestamp(self,):

        t = datetime.datetime.now()
        
        return datetime.datetime(self.year.get(),
                                 self.month.get(),
                                 self.day.get(),
                                 t.hour ,
                                 t.minute,
                                 t.second)
            
        
    def validate(self, action, value_if_allowed, text,):
        # action=1 -> insert
        if(action=='1'):
            if text in '0123456789':
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True          
