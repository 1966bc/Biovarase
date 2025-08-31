#!/usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   var MMXXV
#-----------------------------------------------------------------------------
""" This is the engine module of Biovarase."""
import os
import sys
import inspect
import datetime
import socket


from tools import Tools
from dbms import DBMS
from controller import Controller
from qc import QC
from westgards import Westgards
from exporter import Exporter
from launcher import Launcher

class Engine(DBMS, Controller, QC, Westgards, Exporter, Launcher, Tools):
    def __init__(self, db_name):

        DBMS.__init__(self, db_name)
        Controller.__init__(self)
        QC.__init__(self)
        Westgards.__init__(self)
        Exporter.__init__(self)
        Launcher.__init__(self)
        Tools.__init__(self)
       
        self.dict_instances = {}
        self.poller = None
        self.log_out = None
        self.log_user = {}
        self.no_selected = "Attention!\nNo record selected!"
        self.mandatory = "Attention!\nField %s is mandatory!"
        self.ask_to_delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"
        self.user_not_enable = "User not enabled for this function."
        self.batch_remembers = None
        self.title = "Biovarase"

    def __str__(self):
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__, [x.__name__ for x in Engine.__mro__])

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
        self.launch(path)
        
    def get_python_version(self,):
        return "Python version: %s" % ".".join(map(str, sys.version_info[:3]))

    def get_file(self, file):
        """ return full path of the directory where program resides."""
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

    def on_log(self, function, exc_value, exc_type, module, caller=None):
        """
        Write on log.txt:
        - timestamp
        - Class.method (and caller if exist)
        - Type: message
        - module name
        - traceback current exception
        """
        try:
            
            now = datetime.datetime.now().astimezone()
            
            ts = now.isoformat(sep=" ", timespec="seconds")
            
            module_name = getattr(module, "__name__", str(module))
            
            tb_text = traceback.format_exc()

            header = f"{ts}\n{type(self).__name__}.{function}"
            
            if caller:
                header += f"  (caller: {caller})"

            log_text = (
                f"{header}\n"
                f"{exc_type.__name__}: {exc_value}\n"
                f"{module_name}\n"
                f"{tb_text}\n"
            )

            path = self.get_file("log.txt")
            #fh = file handle
            with open(path, "a", encoding="utf-8", errors="backslashreplace") as fh:
                fh.write(log_text)

        except Exception:
            # il logging non deve mai generare eccezioni
            pass


    def set_ddof(self, value):
        try:
            path = self.get_file('ddof')
            with open(path, 'w') as f:
                f.write(str(value))
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
        
    def get_zscore(self):
        default_zscore = 2.58
        try:
            with open('zscore', 'r') as f:
                v = f.readline().strip()
                return float(v)
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_zscore(self, value):
        try:
            with open('zscore', 'w') as f:
                f.write(str(value))
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            
    def get_section_id(self):
        try:
            path = self.get_file("section_id")
            with open(path, 'r') as f:
                v = f.readline().strip()
                return int(v)
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_section_id(self, value):
        try:
            with open("section_id", "w") as f:
                f.write(str(value))
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            
    def get_remeber_batch_data(self):
        try:
            path = self.get_file("remeber_batch_data")
            with open(path, 'r') as f:
                v = f.readline().strip()
                return int(v)
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_remeber_batch_data(self, value):
        try:
            with open('remeber_batch_data', 'w') as f:
                f.write(str(value))
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
    def get_log_ip(self):
        try:
            return socket.gethostbyname(socket.getfqdn())
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_license(self):
        """get license"""
        try:
            path = self.get_file("LICENSE")
            with open(path, "r") as f:
                v = f.read()
            return v
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_log_id(self):
        try:
            return self.log_user[0]
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None 
        
    def get_observations(self):
        try:
            path = self.get_file('observations')
            with open(path, 'r') as file:
                observations = file.readline().strip()
            return observations
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None 

    def set_observations(self, observations):
        try:
            with open('observations', 'w') as f:
                f.write(str(observations))
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__]) 

    def get_icon(self):
        try:
            path = self.get_file("icon")
            with open(path, "r") as f:
                v = f.readline().strip()
            return v
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None         
            
    def get_expiration_date(self, expiration_date):
        try:
            expiry_date = datetime.datetime.strptime(expiration_date, "%d-%m-%Y").date()
            days_until_expiration = (expiry_date - datetime.date.today()).days
            return days_until_expiration
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None  

    def get_log_time(self):
        return datetime.datetime.now()

    def get_date(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d")

    def get_time(self):
        return datetime.datetime.now().time()

    def get_dimensions(self):
        try:
            dimensions = {}
            path = self.get_file("dimensions")
            with open(path, "r") as filestream:
                for line in filestream:
                    currentline = line.strip().split(",")
                    if len(currentline) == 2:
                        key = currentline[0].strip()
                        value = currentline[1].strip()
                        dimensions[key] = value
                    else:
                        self.on_log(inspect.stack()[0][3],
                                    sys.exc_info()[1],
                                    sys.exc_info()[0],
                                    sys.modules[__name__]) 
            return dimensions
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])            
            return {}

    def get_code_length(self):
        try:
            path = self.get_file("code_length")
            with open(path, "r") as file:
                ret = file.readline().strip()
            return int(ret)
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None 
        
    def get_batch_length(self):
        try:
            path = self.get_file("batch_lenght")
            with open(path, "r") as file:
                ret = file.readline().strip()
            return int(ret)
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None 

    def get_lot_length(self):
        try:
            path = self.get_file("lot_length")
            with open(path, "r") as file:
                ret = file.readline().strip()
            return int(ret)
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None 

    def get_correlation_coefficient(self):
        try:
            path = self.get_file("correlation_coefficient")
            with open(path, "r") as file:
                ret = file.readline().strip()
            return float(ret)
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None 

    def get_bvv(self):
        try:
            path = self.get_file('bvv')
            with open(path, 'r') as f:
                v = f.readline().strip()
            return v
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None 

    def get_user_manual(self):
        try:
            path = self.get_file('manual')
            with open(path, 'r') as f:
                v = f.readline().strip()
            return v
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None 

    def get_qc_thecnical_manual(self):
        try:
            path = self.get_file('qc_thecnical_manual')
            with open(path, 'r') as f:
                v = f.readline().strip()
            return v
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            return None 


def main():

    foo = Engine("biovarase.db")
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
