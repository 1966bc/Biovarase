#!/usr/bin/env python3
"""Provides a primitive light widget to manage calendar date in tkinter projects.

How import;
from calendarium import Calendarium

How instantiate in your frame:

self.start_date = Calendarium(self,"Start Date")

How pack:
#f is a tkinter widget such as Frame,LabelFrame
if use grid method
self.start_date.get_calendarium(f, row, col)
If use pack method
self.start_date.get_calendarium(f,)

Set today date:
self.start_date.set_today()

Check if a date is right formated:

if self.start_date.get_date(self)==False:return

Notice that in the spinbox widget we allowed only integers.
Calendarium use datetime.date to set/get date.

"""
import sys
import datetime
from datetime import date
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


__author__ = "1966bc"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "1.0"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-08-26"
__status__ = "Beta"

class Calendarium(tk.Frame):

    """Provides a primitive light widget to manage calendar date in tkinter projects..

    The __init__ method set the widget, a frame naturally that call this class.

    Note:
        In the spinbox widget we allowed only integers.

    Args:
        msg (str): Human readable string describing the exception.
        code (:obj:`int`, optional): Error code.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """
    def __init__(self, caller, description=None,):
        super().__init__()

        self.set_style()
        self.vcmd = (self.register(self.validate), "%d", "%P", "%S")
        self.caller = caller
        self.description = description

        self.day = tk.IntVar()
        self.month = tk.IntVar()
        self.year = tk.IntVar()

    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )


    def set_style(self):

        self.style = ttk.Style()

        self.style.theme_use("default")

        self.style.configure(".",
                             background=self.get_rgb(240, 240, 237),
                             font=('TkFixedFont'))

        self.style.configure('Calendarium.TLabelframe',
                             relief=tk.GROOVE,
                             padding=2,
                             font=("Helvetica", "10", "bold"),)

        self.style.configure("Calendarium.TSpinbox",
                             background=self.get_rgb(240, 240, 237),
                             arrowcolor="blue",
                             foreground="blue",
                             font="TkFixedFont")


    def get_rgb(self, r, g, b):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        return "#%02x%02x%02x" % (r, g, b)
        
    def get_calendarium(self, container, row=None, col=None):


        w = ttk.LabelFrame(container,
                           style="Calendarium.TLabelframe",
                           text=self.description,
                           borderwidth=1,
                           relief=tk.SUNKEN,)
        # days
        day_label = ttk.LabelFrame(w,
                                   style="Calendarium.TLabelframe",
                                   text="Day",)
        
        self.sp_d = ttk.Spinbox(day_label,
                                style="Calendarium.TSpinbox",
                                width=2,
                                from_=1, to=31,
                                validate="key",
                                validatecommand=self.vcmd,
                                textvariable=self.day,)
        # month
        month_label = ttk.LabelFrame(w,
                                    style="Calendarium.TLabelframe",
                                    text="Month",)
        
        self.sp_m = ttk.Spinbox(month_label,
                                style="Calendarium.TSpinbox",
                                width=2,
                                from_=1, to=12,
                                validate="key",
                                validatecommand=self.vcmd,
                                textvariable=self.month,)
        # year
        year_label = ttk.LabelFrame(w,
                                   style="Calendarium.TLabelframe",
                                   text="Year",)
        
        self.sp_y = ttk.Spinbox(year_label,
                                style="Calendarium.TSpinbox",
                                width=4,
                                validate="key",
                                validatecommand=self.vcmd,
                                from_=1900, to=3000,
                                textvariable=self.year,)

        for p, i in enumerate((day_label, self.sp_d, month_label,
                               self.sp_m, year_label, self.sp_y)):
            if  row is not None:
                i.grid(row=0, column=p, padx=5, pady=5, sticky=tk.W)
            else:
                i.pack(side=tk.LEFT, fill=tk.X, padx=2)

        if row is not None:
            w.grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)
        else:
            w.pack()

        return w

    def set_today(self,):

        today = date.today()

        self.day.set(today.day)
        self.month.set(today.month)
        self.year.set(today.year)

    def get_date(self, caller):

        try:
            return datetime.date(self.year.get(), self.month.get(), self.day.get())
        except ValueError:
            msg = "Date format error:\n{0}".format(sys.exc_info()[1])
            messagebox.showerror(caller.nametowidget(".").title(), msg, parent=caller)
            return False

    def get_timestamp(self,):

        t = datetime.datetime.now()

        return datetime.datetime(self.year.get(),
                                 self.month.get(),
                                 self.day.get(),
                                 t.hour,
                                 t.minute,
                                 t.second)


    def validate(self, action, value, text,):
        # action=1 -> insert
        if action == "1":
            if text in "0123456789":
                try:
                    int(value)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True
