#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" This is the engine module of Biovarase. This class  inherit from other classes."""
import sys
import inspect

from dbms import DBMS
from tools import Tools
from qc import QC
from exporter import Exporter
from launcher import Launcher
from westgards import Westgards


__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"

class Engine(DBMS, Tools, QC, Westgards, Exporter, Launcher,):

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        

        self.args = args
        self.kwargs = kwargs

        self.title = "Biovarase"

        platform = "Developed on Debian Release 9 (stretch) 64-bit"
        s = "%s ver %s\nwritten by\n1966bc\nLocation:\nMilk galaxy\nSolar System\nThird planet(Earth) Italy(Rome)\ngiuseppecostanzi@gmail.com\n%s"
        msg = (s % (self.title, __version__, platform))

        self.about = msg

        self.no_selected = "Attention!\nNo record selected!"
        self.mandatory = "Attention!\nField %s is mandatory!"
        self.delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"
        self.copyleft = "GNU GPL Version 3, 29 June 2007"
        

    def __str__(self):
        return "class: %s\nMRO: %s\ncon: %s" % (self.__class__.__name__,  [x.__name__ for x in Engine.__mro__],self.con)
    
    def get_python_version(self,):
        return "Python version: %s" % ".".join(map(str, sys.version_info[:3]))


    def get_elements(self):

        try:
            f = open('elements', 'r')
            e = f.readline()
            f.close()
            return e
        except:
            self.on_log(self,
                               inspect.stack()[0][3],
                               sys.exc_info()[1],
                               sys.exc_info()[0],
                               sys.modules[__name__])

    def set_elements(self, elements):

        try:
            with open('elements', 'w') as f:
                f.write(str(elements))
           
            
        except:
            self.on_log(self,
                               inspect.stack()[0][3],
                               sys.exc_info()[1],
                               sys.exc_info()[0],
                               sys.modules[__name__])      

    def get_dimensions(self):

        try:
            d = {}
            with open("dimensions", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
                    d[currentline[0]] = currentline[1]

            return d
        except:
            self.on_log(self,
                               inspect.stack()[0][3],
                               sys.exc_info()[1],
                               sys.exc_info()[0],
                               sys.modules[__name__])
def main():

    foo = Engine()
    print(foo)
    elements = foo.get_elements()
    print(elements)
    input('end')

if __name__ == "__main__":
    main()
