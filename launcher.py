# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
# -----------------------------------------------------------------------------

import os
import sys
import inspect
import subprocess
from threading import Thread


class Launcher:
    def __str__(self):
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__,
                                             [x.__name__ for x in Launcher.__mro__])

    def launch(self, path):
        # TO FIX Exception in thread Thread-n: n = 1,2,3,4,...
        #Thread(target=self.open_file(path)).start()
        thread = Thread(target=self.open_file(path), )
        thread.start()


    def open_file(self, path):

        try:
            do_i_exist = os.path.exists(path)

            if do_i_exist:
                if os.name == 'posix':
                    subprocess.call(["xdg-open", path])
                else:
                    os.startfile(path)

        except:
            self.on_log(inspect.stack()[0][3], sys.exc_info()[1], sys.exc_info()[0], sys.modules[__name__])

def main():

    foo = Launcher()
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
