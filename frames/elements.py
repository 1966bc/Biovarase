""" This is the elemets module of Biovarase."""
import tkinter as tk
from tkinter import ttk
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


class Widget(tk.Toplevel):     
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='elements')

        self.parent = parent
        self.engine = kwargs['engine']
        self.resizable(0,0)
        self.elements = tk.IntVar()
        self.vcmd = self.engine.get_validate_integer(self)
        self.init_ui()
        self.engine.center_me(self)

    def init_ui(self):

        f0 = self.engine.get_frame(self, 8)
        
        w = tk.LabelFrame(f0,text='Set elements', font='Helvetica 10 bold')

        self.txElements = ttk.Entry(w, width=8, justify=tk.CENTER,
                                   textvariable=self.elements,
                                   validate = 'key',
                                   validatecommand = self.vcmd)
        self.txElements.pack()

        w.pack(side=tk.LEFT, fill=tk.BOTH,padx=5, pady=5, expand =1)

        bts = [('Save', self.on_save),
               ('Close', self.on_cancel)]

        for btn in bts:
            self.engine.get_button(f0, btn[0] ).bind("<Button-1>", btn[1])

        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self):

        self.elements.set(self.engine.get_elements())
        self.txElements.focus()
        self.title("Set elements")
        
    def on_save(self, evt=None):

        if self.engine.on_fields_control(self)==False:return

        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:
            #notice, same name callback but different class 
            self.engine.set_elements(self.elements.get())
            self.parent.set_elements()
            self.on_cancel()

    def on_cancel(self, evt=None):
        self.destroy()
