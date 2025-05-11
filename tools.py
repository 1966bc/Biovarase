# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXV
# -----------------------------------------------------------------------------

# Refactored Tools class with typing hints and docstrings (English)

import os
import tkinter as tk
from tkinter import messagebox, font, ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from pathlib import Path
from typing import Callable, Optional, Any, Union


class Tools:
    
    def __str__(self) -> str:
        return "class: {0}".format((self.__class__.__name__, ))

    def __init__(self) -> None:
        """Initialize shared style instance."""
        self._style = ttk.Style()

    def set_style(self, style: ttk.Style) -> None:
        """Set a unified theme and styles for the application widgets."""
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

    def get_rgb(self, r: int, g: int, b: int) -> str:
        """Convert RGB integers to a Tkinter-friendly hex color."""
        return "#%02x%02x%02x" % (r, g, b)

    def center_window_relative_to_parent(self, window: Any) -> None:
        """Center a window relative to its parent."""
        parent_x = window.parent.winfo_rootx()
        parent_y = window.parent.winfo_rooty()
        window.geometry("+%d+%d" % (parent_x, parent_y))

    def center_window_on_screen(self, window: Any) -> None:
        """Center a window on the screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_reqwidth()
        window_height = window.winfo_reqheight()
        x = (screen_width - window_width) / 2
        y = (screen_height - window_height) / 2
        window.geometry("+%d+%d" % (x, y))

    def cols_configure(self, w: Any) -> None:
        """Configure three-column grid with proportional weights."""
        w.columnconfigure(0, weight=1)
        w.columnconfigure(1, weight=2)
        w.columnconfigure(2, weight=1)

    def get_init_ui(self, container: Any) -> ttk.Frame:
        """Return a pre-configured frame with default layout settings."""
        w = self.get_frame(container)
        self.cols_configure(w)
        w.grid(row=0, column=0, sticky=tk.N+tk.W+tk.S+tk.E)
        return w

    def get_frame(self, container: Any, style: str = "App.TFrame", padding: Optional[int] = None) -> ttk.Frame:
        """Create a standard ttk.Frame with optional padding and style."""
        return ttk.Frame(container, style=style, padding=padding)
        
    def get_buttons_frame(self, container, padding=None):

        s = ttk.Style()
        s.configure('new.TFrame', background=self.get_rgb(240, 240, 237))
        return ttk.Frame(container,
                         padding=padding,
                         relief=tk.FLAT,
                         style='new.TFrame')

    def get_label_frame(self, container: Any, text: Optional[str] = None,
                        padding: Optional[int] = None) -> ttk.LabelFrame:
        """Create a labeled frame (LabelFrame widget)."""
        return ttk.LabelFrame(container, text=text, relief=tk.GROOVE, padding=padding)

    def get_button(self, container: Any, text: str, underline: int = 0,
                   row: Optional[int] = None, col: Optional[int] = None) -> ttk.Button:
        """Create a button and attach it using grid or pack layout."""
        w = ttk.Button(container, text=text, underline=underline)
        if row is not None and col is not None:
            w.grid(row=row, column=col, sticky=tk.N+tk.W+tk.E, padx=5, pady=5)
        else:
            w.pack(fill=tk.X, padx=5, pady=5)
        return w

    def get_label(self, container: Any, text: str,
                  textvariable: Optional[tk.StringVar] = None,
                  anchor: Optional[str] = None,
                  args: tuple = ()) -> ttk.Label:
        """Create a label with optional grid layout."""
        w = ttk.Label(container, text=text, textvariable=textvariable, anchor=anchor)
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

    def get_scale(self, container: Any, text: str, frm: int, to: int,
                  width: int, var: Optional[tk.Variable] = None,
                  callback: Optional[Callable] = None) -> ttk.LabelFrame:
        """Create a horizontal scale (slider) widget inside a labeled frame."""
        w = self.get_label_frame(container, text=text)
        scale = tk.Scale(w, from_=frm, to=to, orient=tk.HORIZONTAL,
                         variable=var, command=callback)
        scale.pack(anchor=tk.N)
        return w

    def get_radio_buttons(self, container: Any, text: str, ops: list[str],
                          v: tk.Variable, callback: Optional[Callable] = None) -> ttk.LabelFrame:
        """Create a group of radio buttons inside a labeled frame."""
        w = self.get_label_frame(container, text=text)
        for index, label in enumerate(ops):
            ttk.Radiobutton(w, text=label, variable=v,
                            command=callback, value=index).pack(anchor=tk.W)
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

    def get_text_box(self, container: Any, height: Optional[int] = None,
                     width: Optional[int] = None, row: Optional[int] = None,
                     col: Optional[int] = None) -> ScrolledText:
        """Create a scrolled text widget with optional grid layout."""
        w = ScrolledText(container, wrap=tk.WORD, bg='light yellow',
                         relief=tk.GROOVE, height=height, width=width,
                         font='TkFixedFont')
        if row is not None:
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

    def on_fields_control(self, container: Any, title: Optional[str] = None) -> bool:
        """
        Check if all input fields in the container are filled.
        Show a warning if any required fields are empty or invalid.
        Returns True if all fields are valid, False otherwise.
        """
        msg = "Please fill all fields."
        title = title or "My App"

        for w in container.winfo_children():
            for field in w.winfo_children():
                if isinstance(field, (ttk.Entry, tk.Entry, ttk.Combobox)):
                    if not field.get():
                        messagebox.showwarning(title, msg, parent=container)
                        field.focus()
                        return False
                    if isinstance(field, ttk.Combobox):
                        if field.get() not in field.cget('values'):
                            messagebox.showwarning(title, "You can choose only a value from the list.", parent=container)
                            field.focus()
                            return False
        return True

    def get_tree(self, container: Any, cols: list[tuple], size: Optional[int] = None,
                 show: Optional[str] = None) -> ttk.Treeview:
        """Create a Treeview widget with custom column configuration."""
        style = ttk.Style()
        style.map('Treeview', foreground=self.fixed_map('foreground'), background=self.fixed_map('background'))
        style.configure("Treeview.Heading", background="light yellow", font=('TkHeadingFont', 10))
        if size:
            style.configure("Treeview", font=('TkHeadingFont', size))
        headers = [col[1] for col in cols[1:]]
        tree = ttk.Treeview(container, show=show) if show else ttk.Treeview(container)
        tree['columns'] = headers
        tree.tag_configure('is_enable', background='light gray')
        for col in cols:
            tree.heading(col[0], text=col[1], anchor=col[2])
            tree.column(col[0], anchor=col[2], stretch=col[3], minwidth=col[4], width=col[5])
        sb = ttk.Scrollbar(container, command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)
        return tree

    def fixed_map(self, option: str) -> list[tuple]:
        """Fix style map for Treeview to support themed widgets in Tk 8.6.9."""
        style = ttk.Style()
        return [elm for elm in style.map('Treeview', query_opt=option)]

    def get_validate_text(self, caller: Any) -> tuple:
        """Return validation command tuple for text input."""
        return (caller.register(self.validate_text), '%i', '%P')

    def get_validate_integer(self, caller: Any) -> tuple:
        """Return validation tuple for integer fields."""
        return (caller.register(self.validate_integer), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def get_validate_float(self, caller: Any) -> tuple:
        """Return validation tuple for float fields."""
        return (caller.register(self.validate_float), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def limit_chars(self, c: int, v: tk.StringVar, *args: Any) -> None:
        """Limit characters in a StringVar to a given length."""
        if len(v.get()) > c:
            v.set(v.get()[:-1])

    def validate_text(self, index: str, value_if_allowed: str) -> bool:
        """Validate that value is convertible to string."""
        try:
            str(value_if_allowed)
            return True
        except ValueError:
            return False

    def validate_integer(self, action: str, index: str, value_if_allowed: str,
                         prior_value: str, text: str, validation_type: str,
                         trigger_type: str, widget_name: str) -> bool:
        """Validate integer input in real time."""
        if action == '1':
            if text in '0123456789':
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            return False
        return True

    def validate_float(self, action: str, index: str, value_if_allowed: str,
                       prior_value: str, text: str, validation_type: str,
                       trigger_type: str, widget_name: str) -> bool:
        """Validate float input in real time."""
        if action == "1":
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            return False
        return True


    def on_to_assign(self, caller, evt=None):
        msg = "To do!"
        messagebox.showwarning(self.title, msg, )

    def get_widget_attributes(self, container: Any) -> None:
        """Print attributes and their values for each widget in a container."""
        for widg in container.winfo_children():
            print(f'\nWidget Name: {widg.winfo_class()}')
            for key in widg.keys():
                print(f"Attribute: {key:<20} Value: {str(widg[key]):<30} Type: {type(widg[key])}")

    def get_widgets(self, container: Any) -> None:
        """Print each child widget of the container."""
        for widg in container.winfo_children():
            print(widg)
            print(f'\nWidget Name: {widg.winfo_class()}')

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
