# -*- coding: utf-8 -*-
""" This is the westgard launcher of Biovarase.
    It provides to perform the file opening."""
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
__date__ = "2021-03-14"
__status__ = "Production"

class Launcher:
    """This class is used for data export.
    """

    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )

    
    def launch(self, path):

        threading.Thread(target=self.open_file(path), daemon=True).start()    
        
    def open_file(self, path):

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
