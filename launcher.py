#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This is the launcher module of Biovarase. 
It open file generate from Biovarase."""
import os
import subprocess
import threading

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"


class Launcher(threading.Thread):
    def __init__(self,*args, **kwargs):

        super(Launcher, self).__init__( *args, **kwargs)
        
        threading.Thread.__init__(self)

        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return "class: %s\nMRO: %s" % (self.__class__.__name__,  [x.__name__ for x in Launcher.__mro__])        
        
    def run(self):
        self.open_file(self.path)

    def launch(self, path):
        self.path = path
        self.run()

    def open_file(self,path):

        if os.path.exists(path):
            if os.name == 'posix':
                subprocess.call(["xdg-open", path])
            else:
                os.startfile(path)

def main():

    foo = Launcher()
    print(foo)
    input('end')
       
if __name__ == "__main__":
    main()                
