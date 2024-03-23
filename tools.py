# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  microbiotae
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXX
# -----------------------------------------------------------------------------
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from pathlib import Path


class Tools:
    
    def __str__(self):
        return "class: {0}".format((self.__class__.__name__, ))

    def set_style(self, style):

        style.theme_use("clam")

        style.configure(".", background=self.get_rgb(240, 240, 237), font=('TkFixedFont'))

        style.configure('Data.TLabel', font=('Helvetica', 12, 'bold'))

        style.configure("App.TFrame", background=self.get_rgb(240, 240, 237))

        style.configure("StatusBar.TFrame",
                        relief=tk.FLAT,
                        padding=4,
                        background=self.get_rgb(240, 240, 237))

        style.configure('LoggedUser.TLabel',
                        font=("TkDefaultFont", 10, 'bold'),
                        relief=tk.FLAT,
                        foreground='blue',)

        style.configure('StatusBar.TLabel',
                         background=self.get_rgb(240, 240, 237),
                         padding=2,
                         border=1,
                         relief=tk.SUNKEN,
                         font="TkFixedFont")

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
                             padding=5,
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

    def set_me_center(self,caller):
        """center window on the screen"""

        x = caller.parent.winfo_rootx()
        y = caller.parent.winfo_rooty()
        caller.geometry("+%d+%d" % (x, y))    

    def center_me(self, container):

        """center window on the screen"""
        x = (container.winfo_screenwidth() - container.winfo_reqwidth()) / 2
        y = (container.winfo_screenheight() - container.winfo_reqheight()) / 2
        container.geometry("+%d+%d" % (x, y))

    def cols_configure(self, w):

        w.columnconfigure(0, weight=1)
        w.columnconfigure(1, weight=2)
        w.columnconfigure(2, weight=1)

    def get_init_ui(self, container):
        """All insert,update modules have this same configuration on init_ui.
           A Frame, a columnconfigure and a grid method.
           So, why rewrite every time?"""
        w = self.get_frame(container)
        self.cols_configure(w)
        w.grid(row=0, column=0, sticky=tk.N+tk.W+tk.S+tk.E)

        return w

    def get_frame(self, container, style="App.TFrame", padding=None):

        return ttk.Frame(container, padding=padding)
        
    def get_buttons_frame(self, container, padding=None):

        s = ttk.Style()
        s.configure('new.TFrame', background=self.get_rgb(240, 240, 237))
        return ttk.Frame(container,
                         padding=padding,
                         relief=tk.FLAT,
                         style='new.TFrame')

    def get_label_frame(self, container, text=None, padding=None):
        #return tk.LabelFrame(container, text=text, bd=1, relief=tk.RIDGE, padx=5, pady=5,)
        return ttk.LabelFrame(container, text=text, relief=tk.GROOVE, padding=padding)

    def get_button(self, container, text, underline=0, row=None, col=None):
        """button width is set in the option_db file"""
        
        w = ttk.Button(container, text=text, underline=underline)

        if row is not None:
            w.grid(row=row, column=col, sticky=tk.N+tk.W+tk.E, padx=5, pady=5)
        else:
            w.pack(fill=tk.X, padx=5, pady=5)

        return w

    def get_label(self, container, text, textvariable=None, anchor=None, args=()):

        w = ttk.Label(container,
                      text=text,
                      textvariable=textvariable,
                      anchor=anchor)

        if args:
            w.grid(row=args[0], column=args[1], sticky=args[2])
        else:
            w.pack(fill=tk.X, padx=5, pady=5)

        return w

    def get_spin_box(self, container, text, frm, to, width, var=None, callback=None):

        w = self.get_label_frame(container, text=text,)

        tk.Spinbox(w,
                   bg='white',
                   from_=frm,
                   to=to,
                   justify=tk.CENTER,
                   width=width,
                   wrap=False,
                   insertwidth=1,
                   textvariable=var).pack(anchor=tk.CENTER)
        return w

    def get_scale(self, container, text, frm, to, width, var=None, callback=None):

        w = self.get_label_frame(container, text=text,)

        tk.Scale(w,
                 from_=frm,
                 to=to,
                 orient=tk.HORIZONTAL,
                 variable=var).pack(anchor=tk.N)
        return w

    def get_radio_buttons(self, container, text, ops, v, callback=None):

        w = self.get_label_frame(container, text=text)

        for index, text in enumerate(ops):
            ttk.Radiobutton(w,
                            text=text,
                            variable=v,
                            command=callback,
                            value=index,).pack(anchor=tk.W)
        return w

    def set_font(self, family, size, weight=None):

        if weight is not None:
            weight = weight
        else:
            weight = tk.NORMAL

        return font.Font(family=family, size=size, weight=weight)

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
                       yscrollcommand=sb.set,)

        sb.config(command=w.yview)

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)

        return w

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

    def get_save_cancel(self, caller, container, row=None, col=None):

        caller.btnSave = self.get_button(container, "Save", 0, 0, 2)
        caller.btnSave.bind("<KP_Enter>", caller.on_save)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)

        caller.btCancel = self.get_button(container, "Close", 0, 1, 2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-s>", caller.on_save)
        caller.bind("<Alt-c>", caller.on_cancel)


    def get_dir_cancel(self, caller, container):

        caller.btnDir = self.get_button(container, "Choice", 0)
        caller.btnDir.bind("<Button-1>", caller.on_choice_a_dir)
        caller.btCancel = self.get_button(container, "Close", 0)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-h>", caller.on_choice_a_dir)
        caller.bind("<Alt-c>", caller.on_cancel)

           
    def get_save_cancel_delete(self, caller, container):

        caller.btnSave = self.get_button(container, "Save", 0, 0, 2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)

        caller.btDelete = self.get_button(container, "Delete", 0, 1, 2)
        caller.btDelete.bind("<Button-1>", caller.on_delete)

        caller.btCancel = self.get_button(container, "Close", 0, 2, 2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-s>", caller.on_save)
        caller.bind("<Alt-d>", caller.on_delete)
        caller.bind("<Alt-c>", caller.on_cancel)

    def get_add_edit_cancel(self, caller, container):

        caller.btnAdd = self.get_button(container, "Add", 0)
        caller.btnAdd.bind("<Return>", caller.on_add)
        caller.btnAdd.bind("<Button-1>", caller.on_add)
        caller.btnEdit = self.get_button(container, "Edit", 0)
        caller.btnEdit.bind("<Button-1>", caller.on_edit)
        caller.btCancel = self.get_button(container, "Close", 0)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-a>", caller.on_add)
        caller.bind("<Alt-e>", caller.on_edit)
        caller.bind("<Alt-c>", caller.on_cancel)

    def get_add_cancel(self, parent, container):

        parent.btnAdd = self.get_button(container, "Add", 0)
        parent.btnAdd.bind("<Button-1>", parent.on_add)
        parent.btCancel = self.get_button(container, "Close", 0)
        parent.btCancel.bind("<Button-1>", parent.on_cancel)

        parent.bind("<Alt-a>", parent.on_add)
        parent.bind("<Alt-c>", parent.on_cancel)        

    def get_save_reset_cancel(self, caller, container):

        caller.btnSave = self.get_button(container, "Save", 0, 0, 2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)

        caller.btnReset = self.get_button(container, "Reset", 0, 1, 2)
        caller.btnReset.bind("<Button-1>", caller.on_reset)

        caller.btCancel = self.get_button(container, "Close", 0, 2, 2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-s>", caller.on_save)
        caller.bind("<Alt-r>", caller.on_reset)
        caller.bind("<Alt-c>", caller.on_cancel)

    def on_fields_control(self, toplevel, title=None):

        msg = "Please fill all fields."

        if title is not None:
            title = title
        else:
            title ="My App"

        
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

    def get_validate_text(self, caller,):

        return (caller.register(self.validate_text),
                '%i', '%P', )

    def get_validate_integer(self, caller):
        return (caller.register(self.validate_integer),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def get_validate_float(self, caller):
        return (caller.register(self.validate_float),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')


    def limit_chars(self, c, v, *args):
        #print(x,args)
        if len(v.get()) > c:
            v.set(v.get()[:-1])

    def validate_text(self,index, value_if_allowed):
        
        try:
            str(value_if_allowed)
            return True
        except ValueError:
            return False
                 

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

    def on_to_assign(self, caller, evt=None):

        msg = "To do!"
        messagebox.showwarning(self.title, msg, )


    def get_widget_attributes(self, container):
        all_widgets = container.winfo_children()
        for widg in all_widgets:
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            keys = widg.keys()
            for key in keys:
                print("Attribute: {:<20}".format(key), end=' ')
                value = widg[key]
                vtype = type(value)
                print('Value: {:<30} Type: {}'.format(value, str(vtype)))

    def get_widgets(self, container):
        all_widgets = container.winfo_children()
        for widg in all_widgets:
            print(widg)
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            #keys = widg.keys()

    def get_toolbar(self, caller, callbacks):

        toolbar = ttk.Frame(caller,)
        #toolbar = self.get_frame(caller,8)

        for k, v in enumerate(callbacks):
            file = os.path.join('icons', v[0])
            img = tk.PhotoImage(file=self.get_file(file))


            btn = ttk.Button(toolbar,
                             width=20,
                             image=img,
                             command=v[1])
            btn.image = img
            btn.pack(side=tk.TOP, padx=2, pady=2)

        toolbar.pack(side=tk.LEFT, fill=tk.Y, expand=0)

        return  toolbar

    def get_a_pic(self, filename=None):

        if filename is not None:
            if os.path.isfile(filename):
                pass
            else:
                filename = os.path.join('images', 'microbiotae.png')
        else:
            filename = os.path.join('images', 'microbiotae.png')

        image = Image.open(Path(filename))
        #print(image)
        image = image.resize((200, 200), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)

    def get_export_cancel(self, caller, container):

        w = self.get_frame(container,5)
        #get_button(self, container, text, underline=0, row=None, col=None)
        caller.btnExport = self.get_button(w, "Export", 0, 0, 1,)
        caller.btnExport.bind("<Button-1>", caller.on_export)
        caller.btnExport.bind("<Return>", caller.on_export)
    
        caller.btCancel = self.get_button(w, "Close", 0, 1, 1)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-e>", caller.on_export)
        caller.bind("<Alt-c>", caller.on_cancel)

        w.grid(row=0, column=2, sticky=tk.N+tk.E, padx=5, pady=5)


def main():

    foo = Tools()
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
