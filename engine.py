#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018
# version:  0.1                                                                
#-----------------------------------------------------------------------------

import os
import sys

from dbms import DBMS
from widgets import Widgets
from exporter import Exporter
from launcher import Launcher
from westgards import Westgards

class Engine(DBMS, Widgets, Exporter, Launcher, Westgards):

    def __init__(self,*args, **kwargs):

        super(Engine, self).__init__( *args, **kwargs)

        self.args = args
        self.kwargs = kwargs
        
        self.title = "Biovarase"

        self.version = '2.0'
        platform = "Debian Release 9 (stretch) 64-bit"
        s = "%s ver %s\nwritten by\n1966bc\nMilk galaxy\nSolar System\nThird planet(Earth) Italy(Rome)\ngiuseppecostanzi@gmail.com\n%s"
        msg = (s % (self.title, self.version, platform))

        self.about = msg
            
        self.no_selected = "Attention!\nNo record selected!"
        self.mandatory = "Attention!\nField %s is mandatory!"
        self.delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"

        
        self.copyleft = "GNU GPL Version 3, 29 June 2007"
        self.developer = "hal9000\n1966bc mailto[giuseppe.costanzi@gmail.com] \nLocation:\nMilk Galaxy\nSolar System\nThird Planet (Earth)\nItaly\nRome"
        self.description = "welcome %s"%self.title
        self.web = "www.1966bc.wordpress.com"

        
    def __str__(self):
        return "class: %s\nMRO: %s\ncon: %s" % (self.__class__.__name__,  [x.__name__ for x in Engine.__mro__],self.con)

    def get_python_version(self,):
        return "Python version: %s" % ".".join(map(str, sys.version_info[:3]))

    def get_elements(self):
        
        try:

            sql = "SELECT * FROM elements"
        
            rs = self.read(False, sql, ())
          
            return rs[0]
        except:
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])    

       
def main():

    foo = Engine()
    print(foo)
    elements = foo.get_elements()
    print(elements)
    input('end')
       
if __name__ == "__main__":
    main()
