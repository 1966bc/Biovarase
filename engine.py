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
import logging

from tools import Tools
from dbms import DBMS
from controller import Controller
from qc import QC
from westgards import Westgards
from exporter import Exporter
from launcher import Launcher

class Engine(DBMS, Controller, QC, Westgards, Exporter, Launcher, Tools):
    def __init__(self, db_name):

        logging.basicConfig(filename='biovarase.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')
        
        self.logger = logging.getLogger(__name__)

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
        path = self.get_file("biovarase.log") 
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

    def on_log(self, function, exc_value, exc_type, module, level='error',message='message'):
        log_message = f"Errore in {function} (modulo: {module}): {exc_type} - {exc_value} message"
        if level.lower() == 'error':
            self.logger.error(log_message, exc_info=True)
        elif level.lower() == 'warning':
            self.logger.warning(log_message)
        elif level.lower() == 'info':
            self.logger.info(log_message)
        elif level.lower() == 'debug':
            self.logger.debug(log_message)
        elif level.lower() == 'critical':
            self.logger.critical(log_message, exc_info=True)

    def set_ddof(self, value):
        try:
            path = self.get_file('ddof')
            with open(path, 'w') as f:
                f.write(str(value))
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'ddof' not found at path: {path}")
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while writing to 'ddof' file at path: {path}. Error: {ose}")
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while writing to 'ddof': {e}")          

    def get_zscore(self):
        default_zscore = 2.58
        try:
            with open('zscore', 'r') as f:
                v = f.readline().strip()
                return float(v)
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message="File 'zscore' not found. Using default z-score: {default_zscore}")
            return default_zscore
        except ValueError as ve:
            self.on_log(inspect.stack()[0][3], ve, type(ve), sys.modules[__name__], level='warning', message="Invalid value in 'zscore' file. Expected a float. Using default z-score: {default_zscore}")
            return default_zscore
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message="An unexpected error occurred while reading 'zscore'. Using default z-score: {default_zscore}")
            return default_zscore

    def set_zscore(self, value):
        try:
            with open('zscore', 'w') as f:
                f.write(str(value))
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message="Error: 'zscore' file not found while writing.")
        except IOError as ioe:
            self.on_log(inspect.stack()[0][3], ioe, type(ioe), sys.modules[__name__], level='error', message=f"IOError occurred while writing to 'zscore' file: {ioe}")
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while writing to 'zscore': {e}")

    def get_section_id(self):
        try:
            path = self.get_file("section_id")
            with open(path, 'r') as f:
                v = f.readline().strip()
                return int(v)
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'section_id' not found at path: {path}")
            return None
        except ValueError as ve:
            self.on_log(inspect.stack()[0][3], ve, type(ve), sys.modules[__name__], level='warning', message=f"Invalid value in 'section_id' file. Expected an integer at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'section_id' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'section_id' file at path: {path}. Error: {e}")
            return None

    def set_section_id(self, value):
        try:
            with open("section_id", "w") as f:
                f.write(str(value))
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message="Error: 'section_id' file not found while writing.")
        except IOError as ioe:
            self.on_log(inspect.stack()[0][3], ioe, type(ioe), sys.modules[__name__], level='error', message=f"IOError occurred while writing to 'section_id' file: {ioe}")
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while writing to 'section_id': {e}")
            
    def get_remeber_batch_data(self):
        try:
            path = self.get_file("remeber_batch_data")
            with open(path, 'r') as f:
                v = f.readline().strip()
                return int(v)
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'remeber_batch_data' not found at path: {path}")
            return None
        except ValueError as ve:
            self.on_log(inspect.stack()[0][3], ve, type(ve), sys.modules[__name__], level='warning', message=f"Invalid value in 'remeber_batch_data' file. Expected an integer at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'remeber_batch_data' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'remeber_batch_data' file at path: {path}. Error: {e}")
            return None

    def set_remeber_batch_data(self, value):
        try:
            with open('remeber_batch_data', 'w') as f:
                f.write(str(value))
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message="Error: 'remeber_batch_data' file not found while writing.")
        except IOError as ioe:
            self.on_log(inspect.stack()[0][3], ioe, type(ioe), sys.modules[__name__], level='error', message=f"IOError occurred while writing to 'remeber_batch_data' file: {ioe}")
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while writing to 'remeber_batch_data': {e}")            

    def get_log_ip(self):
        try:
            return socket.gethostbyname(socket.getfqdn())
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='warning', message="Could not detect IP address.")
            return "No IP detected."

    def get_license(self):
        """get license"""
        try:
            path = self.get_file("LICENSE")
            with open(path, "r") as f:
                v = f.read()
            return v
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"License file not found at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing license file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading the license file at path: {path}. Error: {e}")
            return None

    def get_log_id(self):
        try:
            return self.log_user[0]
        except IndexError as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='warning', message="self.log_user is empty or does not contain the expected index.")
            return None  # Or raise an exception, depending on your error handling policy
        
    def get_observations(self):
        try:
            path = self.get_file('observations')
            with open(path, 'r') as file:
                observations = file.readline().strip()
            return observations
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'observations' not found at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'observations' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'observations' file at path: {path}. Error: {e}")
            return None

    def set_observations(self, observations):
        try:
            with open('observations', 'w') as f:
                f.write(str(observations))
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message="Error: 'observations' file not found while writing.")
        except IOError as ioe:
            self.on_log(inspect.stack()[0][3], ioe, type(ioe), sys.modules[__name__], level='error', message=f"IOError occurred while writing to 'observations' file: {ioe}")
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while writing to 'observations': {e}")

    def get_icon(self):
        try:
            path = self.get_file("icon")
            with open(path, "r") as f:
                v = f.readline().strip()
            return v
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"Icon file not found at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing icon file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading the icon file at path: {path}. Error: {e}")
            return None

    def get_expiration_date(self, expiration_date):
        try:
            expiry_date = datetime.datetime.strptime(expiration_date, "%d-%m-%Y").date()
            days_until_expiration = (expiry_date - datetime.date.today()).days
            return days_until_expiration
        except ValueError as ve:
            self.on_log(inspect.stack()[0][3], ve, type(ve), sys.modules[__name__], level='warning', message=f"Invalid date format: '{expiration_date}'. Expected format: 'dd-mm-YYYY'.")
            return None
        except TypeError as te:
            self.on_log(inspect.stack()[0][3], te, type(te), sys.modules[__name__], level='warning', message=f"Input 'expiration_date' must be a string. Received: {type(expiration_date)}.")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while processing expiration date: '{expiration_date}'.")
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
                        self.on_log(inspect.stack()[0][3], None, None, sys.modules[__name__], level='warning', message=f"Skipping invalid line in 'dimensions' file: '{line.strip()}'")
            return dimensions
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'dimensions' not found at path: {path}")
            return {}
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'dimensions' file at path: {path}. Error: {ose}")
            return {}
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'dimensions' file at path: {path}. Error: {e}")
            return {}

    def get_code_length(self):
        try:
            path = self.get_file("code_length")
            with open(path, "r") as file:
                ret = file.readline().strip()
            return int(ret)
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'code_length' not found at path: {path}")
            return None
        except ValueError as ve:
            self.on_log(inspect.stack()[0][3], ve, type(ve), sys.modules[__name__], level='warning', message=f"Invalid value in 'code_length' file. Expected an integer at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'code_length' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'code_length' file at path: {path}. Error: {e}")
            return None

    def get_batch_length(self):
        try:
            path = self.get_file("batch_lenght")
            with open(path, "r") as file:
                ret = file.readline().strip()
            return int(ret)
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'batch_lenght' not found at path: {path}")
            return None
        except ValueError as ve:
            self.on_log(inspect.stack()[0][3], ve, type(ve), sys.modules[__name__], level='warning', message=f"Invalid value in 'batch_lenght' file. Expected an integer at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'batch_lenght' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'batch_lenght' file at path: {path}. Error: {e}")
            return None

    def get_lot_length(self):
        try:
            path = self.get_file("lot_length")
            with open(path, "r") as file:
                ret = file.readline().strip()
            return int(ret)
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'lot_length' not found at path: {path}")
            return None
        except ValueError as ve:
            self.on_log(inspect.stack()[0][3], ve, type(ve), sys.modules[__name__], level='warning', message=f"Invalid value in 'lot_length' file. Expected an integer at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'lot_length' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'lot_length' file at path: {path}. Error: {e}")
            return None 

    def get_correlation_coefficient(self):
        try:
            path = self.get_file("correlation_coefficient")
            with open(path, "r") as file:
                ret = file.readline().strip()
            return float(ret)
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'correlation_coefficient' not found at path: {path}")
            return None
        except ValueError as ve:
            self.on_log(inspect.stack()[0][3], ve, type(ve), sys.modules[__name__], level='warning', message=f"Invalid value in 'correlation_coefficient' file. Expected a float at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'correlation_coefficient' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'correlation_coefficient' file at path: {path}. Error: {e}")
            return None

    def get_bvv(self):
        try:
            path = self.get_file('bvv')
            with open(path, 'r') as f:
                v = f.readline().strip()
            return v
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'bvv' not found at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'bvv' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'bvv' file at path: {path}. Error: {e}")
            return None

    def get_user_manual(self):
        try:
            path = self.get_file('manual')
            with open(path, 'r') as f:
                v = f.readline().strip()
            return v
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'manual' not found at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'manual' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'manual' file at path: {path}. Error: {e}")
            return None

    def get_qc_thecnical_manual(self):
        try:
            path = self.get_file('qc_thecnical_manual')
            with open(path, 'r') as f:
                v = f.readline().strip()
            return v
        except FileNotFoundError as fnfe:
            self.on_log(inspect.stack()[0][3], fnfe, type(fnfe), sys.modules[__name__], level='warning', message=f"File 'qc_thecnical_manual' not found at path: {path}")
            return None
        except OSError as ose:
            self.on_log(inspect.stack()[0][3], ose, type(ose), sys.modules[__name__], level='error', message=f"OSError occurred while accessing 'qc_thecnical_manual' file at path: {path}. Error: {ose}")
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred while reading 'qc_thecnical_manual' file at path: {path}. Error: {e}")
            return None


def main():

    foo = Engine("biovarase.db")
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
