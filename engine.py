#!/usr/bin/python
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------
import os
import sys
import shelve
import tkFont
import subprocess

from dbms import DBMS
from westgards import Westgards
from exporter import Exporter
from tooltip import ToolTip

class Engine(DBMS,Westgards,Exporter,ToolTip):
    def __init__(self):
        super(Engine, self).__init__()

        self.title = "Biovarase"

        self.about = "%s\nDeveloped in Python 2.7.9 by:\n1966bc on Debian 8.7 jessie"%self.title

        self.ToolTip = ToolTip

         
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )

    def get_python_version(self,):
        return "Python version: %s" % ".".join(map(str, sys.version_info[:3]))
    

    def get_parameters(self):
        """read parameters file
 
        @param name: none
        @return: dictionary of path, ward_id, supplier_id
        @rtype: dictionary
        """
        
        try:
            d = {}
            path = os.path.join(os.getcwd(),'parameters')
            db = shelve.open(path)
            for k, v in db.items():
                d[k] = (v)
            db.close()
            return d
        except:
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            
            

    def explode_dict(self, obj):
        #for debug...
        for k, v in obj.items():
                print (k,v,type(v))


    def on_fields_control(self, objs):

        for obj in objs:
            if not obj.get():
                ret = False
                break   
            else:
                ret = True
        return ret

    def open_file(self,path):

        if os.path.exists(path):
            if os.name == 'posix':
                subprocess.call(["xdg-open", path])
            else:
                os.startfile(path)
      
   
def main():

    #testing some stuff

    print ("MRO:", [x.__name__ for x in Engine.__mro__])
   
    foo = Engine()

    print (foo)

    raw_input('end')
       
if __name__ == "__main__":
    main()
