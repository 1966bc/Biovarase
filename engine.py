#!/usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
""" This is the engine module of Biovarase."""
import os
import sys
import inspect
import datetime
import socket
import hashlib

from tools import Tools
from dbms import DBMS
from qc import QC
from westgards import Westgards
from exporter import Exporter
from launcher import Launcher


class Engine(DBMS, QC, Westgards, Exporter, Launcher, Tools):
    def __init__(self,):
        super().__init__()

        self.dict_instances = {}
        self.set_connection()
        self.poller = None
        self.log_out = None
        self.log_user = {}
        self.no_selected = "Attention!\nNo record selected!"
        self.mandatory = "Attention!\nField %s is mandatory!"
        self.delete = "Delete data?"
        self.ask_to_delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"
        self.user_not_enable = "User not enabled for this function."
        self.batch_remembers = None
        self.title = "Biovarase"

    def __str__(self):
        return "class: {0}\nMRO: {1}\ncon: {2}".format(self.__class__.__name__,
                                                       [x.__name__ for x in Engine.__mro__],
                                                       self.get_connections)

    def set_instance(self, which, operation, show = False):

        #print(which.winfo_name())

        if operation == 1:
            self.dict_instances[which.winfo_name()] = which.winfo_id()
        else:
            del self.dict_instances[which.winfo_name()]

        if show:
            self.show_istances()

    def get_instance(self, which):

        if  which in self.dict_instances:
            return True
        else:
            return False
        
    def show_istances(self):

        for k, v in self.dict_instances.items():
            print(k, v)
        
    def get_log_file(self):

        path = self.get_file("log.txt") 
        self.open_file(path)
        
    def get_python_version(self,):
        return "Python version: %s" % ".".join(map(str, sys.version_info[:3]))

    def get_file(self, file):
        """# return full path of the directory where program resides."""

        return os.path.join(os.path.dirname(__file__), file)

    def busy(self, caller):
        caller.config(cursor="watch")

    def not_busy(self, caller):
        caller.config(cursor="")

    def set_log_user(self, rs):

        self.log_user.clear()
        for k, v in enumerate(rs):
            #print k,v
            self.log_user[k] = v


    def on_log(self, function, exc_value, exc_type, module):

        now = datetime.datetime.now()
        log_text = "{0}\n{1}\n{2}\n{3}\n{4}\n\n".format(now,
                                                        function,
                                                        exc_value,
                                                        exc_type,
                                                        module)

        path = self.get_file("log.txt")
        log_file = open(path, "a")
        log_file.write(log_text)
        log_file.close()


    def get_ddof(self):
        try:
            f = open('ddof', 'r')
            v = f.readline()
            f.close()
            return int(v)
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_ddof(self, value):

        try:
            with open('ddof', 'w') as f:
                f.write(str(value))

        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])            

    def get_zscore(self):
        try:
            f = open('zscore', 'r')
            v = f.readline()
            f.close()
            return float(v)
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_zscore(self, value):
        try:
            with open('zscore', 'w') as f:
                f.write(str(value))
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_section_id(self):

        try:
            path = self.get_file("section_id")
            f = open(path, 'r')
            v = f.readline()
            f.close()
            return int(v)
        except OSError:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_section_id(self, value):

        try:
            with open("section_id", "w") as f:
                f.write(str(value))

        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            
    def get_remeber_batch_data(self):

        try:
            path = self.get_file("remeber_batch_data")
            f = open(path, 'r')
            v = f.readline()
            f.close()
            return int(v)
        except OSError:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_remeber_batch_data(self, value):

        try:
            with open('remeber_batch_data', 'w') as f:
                f.write(str(value))

        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])                

    def get_log_ip(self):
        return socket.gethostbyname(socket.getfqdn())

    def get_log_time(self):
        return datetime.datetime.now()

    def get_log_id(self):
        return self.log_user[0]

    def get_license(self):
        """get license"""
        try:
            path = self.get_file("LICENSE")
            f = open(path, "r")
            v = f.read()
            f.close()
            return v
        except FileNotFoundError:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_date(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d")

    def get_time(self):
        return datetime.datetime.now().time()

    def get_elements(self):
        
        try:
            file = open('elements', 'r')
            ret = file.readline()
            file.close()
            return ret
        except FileNotFoundError:
            self.on_log(self,
                       inspect.stack()[0][3],
                       sys.exc_info()[1],
                       sys.exc_info()[0],
                       sys.modules[__name__])

    def set_elements(self, elements):

        try:
            with open('elements', 'w') as f:
                f.write(str(elements))

        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_icon(self):

        try:
            path = self.get_file("icon")
            f = open(path, "r")
            v = f.readline()
            f.close()
            return v

        except FileNotFoundError:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_expiration_date(self, expiration_date):
        return (datetime.datetime.strptime(expiration_date, "%d-%m-%Y").date() - datetime.date.today()).days

    def get_password(self, s):

        password = hashlib.md5()
        password.update(s.strip().encode("utf-8"))
        encripted = password.hexdigest()
        return encripted

    def get_encript_password(self, password):

        password = password.strip()

        return hashlib.md5(password.encode()).hexdigest()

    def get_dimensions(self):

        try:
            d = {}
            with open("dimensions", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
                    d[currentline[0]] = currentline[1]
            return d
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_code_length(self):

        try:
            file = open("code_length", "r")
            ret = file.readline()
            file.close()
            return int(ret)
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])            


def main():

    foo = Engine()
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
