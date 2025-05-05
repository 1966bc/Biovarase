#!/usr/bin/env python3
"""
Calendarium - A primitive calendar date widget for Tkinter projects.

Usage:
    from calendarium import Calendarium

    self.start_date = Calendarium(self, "Start Date")
    self.start_date.get_calendarium(parent_frame, row=0, col=0)  # grid method
    self.start_date.get_calendarium(parent_frame)  # pack method

Features:
    - Set current date.
    - Validate and retrieve selected date.
    - Get a timestamp with current time.

Author: Giuseppe Costanzi (1966bc)
License: GNU GPL v3
Version: 1.0
"""

import sys
import datetime
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Union


class Calendarium(tk.Frame):
    def __init__(self, caller: tk.Widget, name: str) -> None:
        super().__init__()
        self.vcmd = (self.register(self.validate), '%d', '%P', '%S')

        self.caller = caller
        self.name = name

        self.day = tk.IntVar()
        self.month = tk.IntVar()
        self.year = tk.IntVar()

    def __str__(self) -> str:
        return f"class: {self.__class__.__name__}"

    def get_calendarium(self, container: tk.Widget, row: Optional[int] = None, col: Optional[int] = None) -> tk.LabelFrame:
        frame = tk.LabelFrame(
            container,
            text=self.name,
            borderwidth=1,
            padx=2,
            pady=2,
            relief=tk.GROOVE,
        )

        day_frame = tk.LabelFrame(frame, text="Day")
        day_spinbox = tk.Spinbox(
            day_frame, width=2, from_=1, to=31,
            validate='key', validatecommand=self.vcmd,
            textvariable=self.day, bg='white', fg='blue', relief=tk.GROOVE
        )

        month_frame = tk.LabelFrame(frame, text="Month")
        month_spinbox = tk.Spinbox(
            month_frame, width=2, from_=1, to=12,
            validate='key', validatecommand=self.vcmd,
            textvariable=self.month, bg='white', fg='blue', relief=tk.GROOVE
        )

        year_frame = tk.LabelFrame(frame, text="Year")
        year_spinbox = tk.Spinbox(
            year_frame, width=4, from_=1900, to=3000,
            validate='key', validatecommand=self.vcmd,
            textvariable=self.year, bg='white', fg='blue', relief=tk.GROOVE
        )

        widgets = [day_frame, day_spinbox, month_frame, month_spinbox, year_frame, year_spinbox]

        for idx, widget in enumerate(widgets):
            if row is not None and col is not None:
                widget.grid(row=0, column=idx, padx=5, pady=5, sticky=tk.W)
            else:
                widget.pack(side=tk.LEFT, fill=tk.X, padx=2)

        if row is not None and col is not None:
            frame.grid(row=row, column=col, sticky=tk.W)
        else:
            frame.pack()

        return frame

    def set_today(self):
        today = datetime.date.today()
        self.day.set(today.day)
        self.month.set(today.month)
        self.year.set(today.year)

    def get_date(self, caller: tk.Widget) -> Union[datetime.date, bool]:
        try:
            return datetime.date(self.year.get(), self.month.get(), self.day.get())
        except ValueError as e:
            messagebox.showerror(caller.title(), f"Date format error:\n{e}", parent=caller)
            return False

    def get_timestamp(self) -> datetime.datetime:
        now = datetime.datetime.now()
        return datetime.datetime(
            self.year.get(), self.month.get(), self.day.get(),
            now.hour, now.minute, now.second
        )

    def validate(self, action: str, value: str, text: str) -> bool:
        if action == '1':
            if text.isdigit():
                try:
                    int(value)
                    return True
                except ValueError:
                    return False
            return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calendarium Demo")

    cal = Calendarium(root, "Select Date")
    cal_frame = cal.get_calendarium(root)
    cal.set_today()

    def show_date():
        result = cal.get_date(root)
        if result:
            messagebox.showinfo("Selected Date", str(result))

    def show_timestamp():
        result = cal.get_timestamp()
        messagebox.showinfo("Timestamp", str(result))

    tk.Button(root, text="Get Date", command=show_date).pack(pady=5)
    tk.Button(root, text="Get Timestamp", command=show_timestamp).pack(pady=5)

    root.mainloop()


# unittest
import unittest

class TestCalendarium(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.cal = Calendarium(self.root, "Test Date")

    def tearDown(self):
        self.root.destroy()

    def test_set_today(self):
        today = datetime.date.today()
        self.cal.set_today()
        self.assertEqual(self.cal.day.get(), today.day)
        self.assertEqual(self.cal.month.get(), today.month)
        self.assertEqual(self.cal.year.get(), today.year)

    def test_get_valid_date(self):
        self.cal.day.set(15)
        self.cal.month.set(6)
        self.cal.year.set(2025)
        date_obj = self.cal.get_date(self.root)
        self.assertEqual(date_obj, datetime.date(2025, 6, 15))

    def test_get_invalid_date(self):
        self.cal.day.set(31)
        self.cal.month.set(2)
        self.cal.year.set(2025)
        result = self.cal.get_date(self.root)
        self.assertFalse(result)

    def test_get_timestamp(self):
        self.cal.day.set(1)
        self.cal.month.set(1)
        self.cal.year.set(2025)
        ts = self.cal.get_timestamp()
        self.assertEqual(ts.year, 2025)
        self.assertEqual(ts.month, 1)
        self.assertEqual(ts.day, 1)


if __name__ == "__main__":
    unittest.main()
