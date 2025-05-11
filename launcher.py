# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV
# -----------------------------------------------------------------------------

import os
import sys
import inspect
import subprocess
from threading import Thread
import logging


class Launcher:
    def __init__(self):
        self.launch_result = None  # Initialize result attribute

    def __str__(self):
        return "class: {0}\nMRO: {1}".format(
            self.__class__.__name__, [x.__name__ for x in Launcher.__mro__]
        )

    def launch(self, path):
        thread = Thread(target=self._open_file, args=(path,))
        thread.start()
        thread.join()  # Wait for the thread to complete
        return self.launch_result  # Return the result

    def _open_file(self, path):
        try:
            if os.path.exists(path):
                if os.name == "posix":
                    subprocess.call(["xdg-open", path])
                elif os.name == "nt":  # 'nt' stay for Windows
                    os.startfile(path)
                self.launch_result = True  # Indicate success
            else:
                raise FileNotFoundError(f"File not found: {path}")

        except FileNotFoundError as fnf_error:
            self.on_log(
                inspect.stack()[0][3],
                fnf_error,
                type(fnf_error),
                sys.modules[__name__],
            )
            self.launch_result = False  # Indicate failure
        except subprocess.CalledProcessError as subproc_error:
            self.on_log(
                inspect.stack()[0][3],
                subproc_error,
                type(subproc_error),
                sys.modules[__name__]
                )
            self.launch_result = False
        except OSError as os_error:
            self.on_log(
                inspect.stack()[0][3],
                os_error,
                type(os_error),
                sys.modules[__name__]
            )
            self.launch_result = False
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"An unexpected error occurred while opening file: {e}",
            )
            self.launch_result = False
