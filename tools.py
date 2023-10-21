# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk

class Tools:
    
    def __str__(self):
        return "class: {0}".format((self.__class__.__name__, ))

    def set_style(self, style):

        style.theme_use("clam")

        style.configure(".", background=self.get_rgb(240, 240, 237), font=('TkFixedFont'))

        style.configure('Data.TLabel', font=('Helvetica', 12, 'bold'))

        style.configure("App.TFrame", background=self.get_rgb(240, 240, 237))

        style.configure("App.TLabel",
                             background=self.get_rgb(240, 240, 237),
                             padding=2,
                             anchor=tk.W,
                             font="TkFixedFont")

        style.configure("App.TLabelframe",
                             background=self.get_rgb(240, 240, 237),
                             relief=tk.GROOVE,
                             padding=2,
                             font="TkFixedFont")

        style.configure("App.TButton",
                             background=self.get_rgb(240, 240, 237),
                             padding=8,
                             border=1,
                             relief=tk.RAISED,
                             font="TkFixedFont")

        style.configure("Buttons.TFrame",
                             background=self.get_rgb(240, 240, 237),
                             padding=8,
                             relief=tk.GROOVE,)
        
        style.configure('App.TRadiobutton',
                             background=self.get_rgb(240, 240, 237),
                             padding=4,
                             font="TkFixedFont")

        style.configure('App.TCombobox',
                             background=self.get_rgb(240, 240, 237),
                             font="TkFixedFont")

        style.configure('StatusBar.TLabel',
                             background=self.get_rgb(240, 240, 237),
                             padding=2,
                             border=1,
                             relief=tk.SUNKEN,
                             font="TkFixedFont")

        style.map('Treeview',
                       foreground=self.fixed_map('foreground'),
                       background=self.fixed_map('background'))

        style.configure("Treeview.Heading",
                             background=self.get_rgb(240, 240, 237),
                              font=("TkFixedFont", "10", "italic"),)

        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        style.configure("Mandatory.TLabel",
                             foreground=self.get_rgb(0, 0, 255),
                             background=self.get_rgb(255, 255, 255))

        style.configure('Target.TLabel',
                    foreground=self.get_rgb(255, 69, 0),
                    background=self.get_rgb(255, 255, 255))

        ##1966BC Color Hex  (25,102,188)
        style.configure('Average.TLabel',
                    foreground=self.get_rgb(25, 102, 188),
                    background=self.get_rgb(255, 255, 255))

        style.configure('westgard_violation.TLabel',
                        background=self.get_rgb(255, 106, 106),)

        style.configure('westgard_ok.TLabel',
                        background=self.get_rgb(152, 251, 152))

        style.configure('Statusbar.TLabel',
                        foreground='blue',)

        style.configure('black_and_withe.TLabel',
                    background=self.get_rgb(255, 255, 255),
                    foreground=self.get_rgb(77, 77, 77),)

    def get_rgb(self, r, g, b):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        return "#%02x%02x%02x" % (r, g, b)

    def center_me(self, container):

        """center window on the screen"""
        x = (container.winfo_screenwidth() - container.winfo_reqwidth()) / 2
        y = (container.winfo_screenheight() - container.winfo_reqheight()) / 2
        container.geometry("+%d+%d" % (x, y))

    def set_font(self, family, size, weight=None):

        if weight is not None:
            weight = weight
        else:
            weight = tk.NORMAL

        return font.Font(family=family, size=size, weight=weight)

    def get_text_box(self, container, height=None, width=None, row=None, col=None):

        w = ScrolledText(container,
                         wrap = tk.WORD,
                         bg='light yellow',
                         relief=tk.GROOVE,
                         height=height,
                         width=width,
                         font='TkFixedFont',)

        if row is not None:
            #print(row,col)
            w.grid(row=row, column=1, sticky=tk.W)
        else:
            w.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        return w

    def on_fields_control(self, toplevel, title=None):

        msg = "Please fill all fields."

        if title is not None:
            title = title
        else:
            title = self.title
        #print(toplevel)
        for w in toplevel.winfo_children():
            #print(w)
            for field in w.winfo_children():
                #print(field)
                if type(field) in(ttk.Entry, tk.Entry, ttk.Combobox):
                    if not field.get():
                        messagebox.showwarning(title, msg, parent=toplevel)
                        field.focus()
                        return 0
                    elif type(field) == ttk.Combobox:
                        if field.get() not in field.cget('values'):
                            msg = "You can choice only a value of the list."
                            messagebox.showwarning(title, msg, parent=toplevel)
                            field.focus()
                            return 0
                        
    def get_tree(self, container, cols, size=None, show=None):

        #this is a patch because with tkinter version with Tk 8.6.9 the color assignment with tags dosen't work
        #https://bugs.python.org/issue36468
        style = ttk.Style()

        style.map('Treeview', foreground=self.fixed_map('foreground'), background=self.fixed_map('background'))

        style.configure("Treeview.Heading", background="light yellow")

        style.configure("Treeview.Heading", font=('TkHeadingFont', 10))

        if size is not None:
            style.configure("Treeview",
                            highlightthickness=0,
                            bd=0,
                            font=('TkHeadingFont', size)) # Modify the font of the body
        else:
            pass

        headers = []

        for col in cols:
            headers.append(col[1])
        del headers[0]

        if show is not None:
            w = ttk.Treeview(container, show=show)

        else:
            w = ttk.Treeview(container,)

        w['columns'] = headers
        w.tag_configure('is_enable', background='light gray')

        for col in cols:
            w.heading(col[0], text=col[1], anchor=col[2],)
            w.column(col[0], anchor=col[2], stretch=col[3], minwidth=col[4], width=col[5])

        sb = ttk.Scrollbar(container)
        sb.configure(command=w.yview)
        w.configure(yscrollcommand=sb.set)

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)

        return w

    def fixed_map(self, option):

        style = ttk.Style()
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in style.map('Treeview', query_opt=option) if
                elm[:2] != ('!disabled', '!selected')]

    
    def get_validate_integer(self, caller):
        return (caller.register(self.validate_integer),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def get_validate_float(self, caller):
        return (caller.register(self.validate_float),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
     
    def limit_chars(self, c, v, *args):
        #print(c,v,args)
        if len(v.get()) > c:
            v.set(v.get()[:-1])

    def validate_integer(self, action, index, value_if_allowed,
                         prior_value, text, validation_type,
                         trigger_type, widget_name):
        # action=1 -> insert
        if action == '1':
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

    def validate_float(self, action, index, value_if_allowed,
                       prior_value, text, validation_type,
                       trigger_type, widget_name):
        # action=1 -> insert
        if action == "1":
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def get_listbox(self, container, height=None, width=None, color=None):

        sb = ttk.Scrollbar(container, orient=tk.VERTICAL)

        w = tk.Listbox(container,
                       relief=tk.GROOVE,
                       selectmode=tk.EXTENDED,
                       exportselection=0,
                       height=height,
                       width=width,
                       background=color,
                       font='TkFixedFont',
                       #bg="white",
                       #fg="black",
                       yscrollcommand=sb.set,)

        sb.config(command=w.yview)

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)

        return w        

def main():

    foo = Tools()
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
