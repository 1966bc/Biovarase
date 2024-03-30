#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
# -----------------------------------------------------------------------------
import hashlib
import threading
from time import sleep
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from engine import Engine
import frames.main as ui

__author__ = "1966bc"
__copyright__ = "Copyleft"
__credits__ = ["hal9000", "Richard Barasa"]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "1.618"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "hiems MMXXIII"
__status__ = "Demo"


class Monitor(threading.Thread):

    def __init__(self, parent):
        threading.Thread.__init__(self)

        self.check = True
        self.parent = parent
        self.idle = 0
        self.old_coord = None

    def stop(self):
        self.check = False

    def run(self):

        while self.check:

            if not self.check:
                break
            else:
                coord = self.parent.winfo_pointerxy()

                if self.old_coord != coord:
                    self.old_coord = coord
                    self.idle = 0
                else:
                    self.idle += 1

                #print(self.idle)                    

                if self.idle == (int(self.parent.nametowidget(".").engine.log_user[6])*60):

                    self.check = False
                    self.parent.after(1000, self.parent.on_quit)
                else:
                    sleep(1)


class Login(ttk.Frame):

    def __init__(self, parent,):
        super().__init__()

        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW",
                             self.nametowidget(".").on_exit)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.nick = tk.StringVar()
        self.password = tk.StringVar()
        self.attempts = 0
        self.nametowidget(".").engine.thread = None
        self.center_me()
        self.init_ui()

    def center_me(self):
        """Center window on the screen."""
        x = (self.parent.winfo_screenwidth() - self.parent.winfo_reqwidth()) / 2
        y = (self.parent.winfo_screenheight() - self.parent.winfo_reqheight()) / 2
        self.parent.geometry("+%d+%d" % (x, y))

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}

        self.frm_main = ttk.Frame(self.parent, style="App.TFrame")
        self.frm_main.grid(row=0, column=0)

        w = ttk.Frame(self.frm_main, style="App.TFrame", padding=8)
        w.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        ttk.Label(w, text="Login:",).grid(row=r, sticky=tk.W, **paddings)
        self.txtNick = ttk.Entry(w, textvariable=self.nick,)
        self.txtNick.grid(row=r, column=c, **paddings)

        r += 1
        ttk.Label(w, text="Password:",).grid(row=r, sticky=tk.W, **paddings)
        ent_password = ttk.Entry(w, show="*", textvariable=self.password)
        ent_password.grid(row=r, column=c, **paddings)

        r += 1
        c = 0
        btn_login = ttk.Button(w, style="App.TButton", text="Login", underline=0)
        btn_login.bind("<Return>", self.on_login)
        btn_login.bind("<Button-1>", self.on_login)
        btn_login.bind("<Alt-l>", self.on_login)
        self.parent.bind("<Alt-l>", self.on_login)
        btn_login.grid(row=r, column=c, sticky=tk.W, **paddings)

        c += 1
        btn_exit = ttk.Button(w, style="App.TButton", text="Cancel", underline=0)
        btn_exit.bind("<Button-1>", self.parent.on_exit)
        btn_exit.bind("<Alt-c>", self.parent.on_exit)
        self.parent.bind("<Alt-c>", self.parent.on_exit)
        btn_exit.grid(row=r, column=c, sticky=tk.W, **paddings)

    def on_open(self,):

        self.txtNick.focus()

    def hide(self):
        """Hide login frame if login succesful."""
        self.parent.withdraw()

    def get_values(self,):
        """Retrive variables and encript password."""
        nick = self.nick.get()
        password = self.password.get()
        password.strip()
        encripted = hashlib.md5(password.encode()).hexdigest()

        return (nick, encripted)

    def on_login(self, event=None):
        """Try to log ;)"""

        if self.nametowidget(".").engine.on_fields_control(self.frm_main,
                                                           self.nametowidget(".").title()) == False: return

        args = self.get_values()

        rs = self.nametowidget(".").engine.login(args)
        
        if rs:
            self.nametowidget(".").engine.set_log_user(rs)            
            self.hide()
            
            if self.nametowidget(".").engine.log_user[7] == True:
                self.nametowidget(".").engine.thread = Monitor(self)
                self.nametowidget(".").engine.thread.start()

            ui.Main(self).on_open()
            
        else:
            msg = "Login failed."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

            if self.attempts > 1:
                msg = "Max login attempts\nContact system admin!"
                messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
                self.on_quit()

            else:
                self.attempts += 1
                self.txtNick.focus()

    def on_about(self,):
        messagebox.showinfo(self.nametowidget(".").title(),
                            self.nametowidget(".").info,
                            parent=self)

    def on_quit(self, evt=None):
        self.nametowidget(".").engine.con.close()
        self.quit()


class App(tk.Tk):
    """Main Application start here"""
    def __init__(self):
        super().__init__()

        self.resizable(0, 0)
        self.engine = Engine()
        self.set_style()
        self.title("Biovarase")
        self.set_info()
        self.set_icon()
        
        obj = Login(self,)
        obj.on_open()

    def set_style(self,):
        self.style = ttk.Style()
        self.engine.set_style(self.style)
        
    def set_info(self,):
        msg = "{0}\nauthor: {1}\ncopyright: {2}\ncredits: {3}\nlicense: {4}\nversion: {5}\
               \nmaintainer: {6}\nemail: {7}\ndate: {8}\nstatus: {9}"
        self.info = msg.format(self.title(),
                          __author__,
                          __copyright__,
                          __credits__,
                          __license__,
                          __version__,
                          __maintainer__,
                          __email__,
                          __date__,
                          __status__)

    def set_icon(self):
        icon = tk.PhotoImage(data=self.engine.get_icon())
        self.call("wm", "iconphoto", self._w, "-default", icon)

    def on_exit(self, evt=None):

        msg = "Do you want to quit {0}?".format(self.nametowidget(".").title())
        if messagebox.askokcancel(self.nametowidget(".").title(), msg, parent=self):
            try:
                self.nametowidget(".").engine.con.close()
                if self.nametowidget(".").engine.thread is not None:
                    self.nametowidget(".").engine.thread.stop()
            except:
                pass
            finally:
                self.nametowidget(".").engine.batch_remembers = None
                self.quit()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()

