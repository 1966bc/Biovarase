""" This is the analytical module of Biovarase.
It shows analyticak goals rules"""
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
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='analitical')

        self.parent = parent
        self.engine = kwargs['engine']

        self.attributes('-topmost', True)
        self.resizable(0,0)
    
        self.init_ui()
        self.engine.center_me(self)

    def init_ui(self):

        w = self.engine.get_init_ui(self)
        
        tk.Label(w, text="k CV:").grid(row=0, sticky=tk.W,padx=10,pady=10)
        tk.Label(w,bg='green', text="0.25").grid(row=1,column=0,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,bg='yellow', text="0.50").grid(row=2,column=0,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,bg='red', text="0.75").grid(row=3,column=0,sticky=tk.W,padx=10,pady=10)

        tk.Label(w, text="k Bias:").grid(row=0,column=1, sticky=tk.W,padx=10,pady=10)
        tk.Label(w,bg='green', text="0.125<= k <= 0.25").grid(row=1,column=1,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,bg='yellow', text="0.25<= k <= 0.375").grid(row=2,column=1,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,bg='red', text="k > 0.375").grid(row=3,column=1,sticky=tk.W,padx=10,pady=10)

        tk.Label(w, text="Eta:").grid(row=0,column=2, sticky=tk.W,padx=10,pady=10)
        tk.Label(w,bg='green', text="ETa < 1.65 (0.25 CVi) + 0.125 (CVi2+ CVg2) ½ ").grid(row=1,column=2,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,bg='yellow', text="ETa < 1.65 (0.50 CVi) + 0.25 (CVi2 + CVg2) ½").grid(row=2,column=2,sticky=tk.W,padx=10,pady=10)
        tk.Label(w,bg='red', text="ETa < 1.65 (0.75 CVi) + 0.375 (CVi2+ CVg2) ½").grid(row=3,column=2,sticky=tk.W,padx=10,pady=10)

    def on_open(self,):

        self.title("Analytical Goals Explained")
        
         
    def on_cancel(self, evt=None):
        self.destroy()
