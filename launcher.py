#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018
# version:  0.1                                                                
#-----------------------------------------------------------------------------
import os
import subprocess
import threading

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
