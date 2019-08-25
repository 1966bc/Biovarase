""" This is the analytical module of Biovarase."""
import tkinter as tk

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-24"
__status__ = "Production"

class Widget(tk.Toplevel):     
    def __init__(self,parent, engine, index = None):
        super().__init__(name='zscore')  

        self.attributes('-topmost', True)
        self.transient(parent)
        self.resizable(0,0)
        self.engine = engine
        self.engine.center_me(self)
        self.init_ui()

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        tk.Label(w, text="Z-Score").grid(row=0, sticky=tk.W,padx=10,pady=10)
        tk.Label(w, text="2.33").grid(row=1,column=0,sticky=tk.W,padx=10,pady=10)
        tk.Label(w, text="2.05").grid(row=2,column=0,sticky=tk.W,padx=10,pady=10)
        tk.Label(w, text="1.88").grid(row=3,column=0,sticky=tk.W,padx=10,pady=10)
        tk.Label(w, text="1.75").grid(row=4,column=0,sticky=tk.W,padx=10,pady=10)
        tk.Label(w, text="1.65").grid(row=5,column=0,sticky=tk.W,padx=10,pady=10)

        tk.Label(w,text="Probability").grid(row=0,column=1, sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="p>0.01").grid(row=1,column=1,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="p>0.02").grid(row=2,column=1,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="p>0.03").grid(row=3,column=1,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="p>0.04").grid(row=4,column=1,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="p>0.05").grid(row=5,column=1,sticky=tk.W,padx=10,pady=10)

        tk.Label(w, text="Probability").grid(row=0,column=2, sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="99%").grid(row=1,column=2,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="98%").grid(row=2,column=2,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="97%").grid(row=3,column=2,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="96%").grid(row=4,column=2,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,text="95%").grid(row=5,column=2,sticky=tk.W,padx=10,pady=10)

       

    def on_open(self,):

        self.title("Probability")
        
         
    def on_cancel(self, evt=None):
        self.destroy()
