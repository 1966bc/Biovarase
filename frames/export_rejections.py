""" This is the export_rejections module of Biovarase."""
import tkinter as tk
from tkinter import messagebox

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"


class Dialog(tk.Toplevel):     
    def __init__(self,parent, engine, index=None):
        super().__init__(name='export_rejection')  

        self.attributes('-topmost', True)
        self.resizable(0,0)
        self.transient(parent) 
        self.parent = parent
        self.engine = engine
        self.index = index
        self.day =  tk.IntVar()
        self.month =  tk.IntVar()
        self.year =  tk.IntVar()
        self.init_ui()

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r =0
        tk.Label(w, text="Export From:").grid(row=r,sticky=tk.W)

        r +=1
        self.engine.get_calendar(self, w, r,)

        self.engine.get_export_cancel(self, w)


    def on_open(self):

        self.engine.set_calendar_date(self)

        self.title("Export Rejections Data")
        
    def on_export(self, evt=None):

        if self.engine.get_calendar_date(self)==False:return
        if messagebox.askyesno(self.engine.title, "Export data?", parent=self) == True:

            args = (self.engine.get_calendar_date(self),)
            self.engine.get_rejections(args)
    
    def on_cancel(self, evt=None):
        self.destroy()

