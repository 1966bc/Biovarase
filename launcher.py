# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV
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
        thread = Thread(target=self._open_file, args=(path,))
        thread.start()

    def _open_file(self, path):
        try:
            if os.path.exists(path):
                if os.name == 'posix':
                    subprocess.call(["xdg-open", path])
                elif os.name == 'nt':  # 'nt' stay for Windows
                    os.startfile(path)
            else:
                self.on_log(inspect.stack()[0][3], f"File non trovato: {path}", FileNotFoundError, sys.modules[__name__])
        except:
            self.on_log(inspect.stack()[0][3], sys.exc_info()[1], sys.exc_info()[0], sys.modules[__name__])

def main():
    foo = Launcher()
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
