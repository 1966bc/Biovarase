#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" This is the engine of Biovarase. This module show inheritance.
This class  inherit from other classes."""
import sys
import inspect
import time
import numpy as np
import math

from dbms import DBMS
from tools import Tools
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

class Engine(DBMS, Tools, Westgards, Exporter, Launcher,):

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        

        self.args = args
        self.kwargs = kwargs

        self.title = "Biovarase"

        platform = "Developed on Debian Release 9 (stretch) 64-bit"
        s = "%s ver %s\nwritten by\n1966bc\nMilk galaxy\nSolar System\nThird planet(Earth) Italy(Rome)\ngiuseppecostanzi@gmail.com\n%s"
        msg = (s % (self.title, __version__, platform))

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
            f = open('elements', 'r')
            e = f.readline()
            f.close()
            return e
        except:
            self.engine.on_log(self,
                               inspect.stack()[0][3],
                               sys.exc_info()[1],
                               sys.exc_info()[0],
                               sys.modules[__name__])

    def set_elements(self, elements):

        try:
            with open('elements', 'w') as f:
                f.write(str(elements))
           
            
        except:
            self.engine.on_log(self,
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
            self.engine.on_log(self,
                               inspect.stack()[0][3],
                               sys.exc_info()[1],
                               sys.exc_info()[0],
                               sys.modules[__name__])


    def get_qc(self, target, sd, rs):


        try:

            dates = []
            x_labels = []
            series = []

            count_rs = len(rs)

            rs = tuple(i for i in rs if i[4]!=0)

            if rs:

                for i in reversed(rs):
                    #print(i)
                    series.append(i[1])
                    x_labels.append(i[2])
                    dates.append(i[3])

                count_series = len(series)
                compute_average = round(np.mean(series),2)
                compute_sd = round(np.std(series),2)
                compute_cv = round((compute_sd/compute_average)*100,2)
                compute_bias = round((compute_average-target)/(target)*100,2)
                compute_range = round(np.ptp(series),2)

                return (count_rs, target, sd, series, count_series,
                        compute_average, compute_sd, compute_cv, compute_bias,
                        compute_range, x_labels, dates)
           

            else:
                return None
        except:
             self.engine.on_log(self,
                               inspect.stack()[0][3],
                               sys.exc_info()[1],
                               sys.exc_info()[0],
                               sys.modules[__name__])


    def get_series(self, batch_id):

        series = []

        e = self.get_elements()

        args = (batch_id, e)

        sql = "SELECT ROUND(result,2)\
               FROM results\
               WHERE batch_id =?\
               AND enable =1\
               ORDER BY recived DESC\
               LIMIT ?"

        rs = self.read(True, sql, args)

        for i in reversed(rs):
            series.append(i[0])

        return series

    def get_stat(self, batch_id, limit,):


        try:

            sql = "SELECT result_id,\
                          ROUND(result,2)\
                   FROM results\
                   WHERE batch_id =?\
                   AND enable =1\
                   ORDER BY result_id DESC\
                   LIMIT ?"

            args = (batch_id, limit)
            rs = self.read(True, sql, args)

            results=[]
            if len(rs) > 5:
                for i in rs:
                    results.append(float(i[1]))

                avg = round(np.mean(results),2)
                sd = round(np.std(results),2)
                cv = (sd/avg)*100

                return len(rs),cv,avg,sd
            else:
                return False
        except:
            self.engine.on_log(self,
                               inspect.stack()[0][3],
                               sys.exc_info()[1],
                               sys.exc_info()[0],
                               sys.modules[__name__])
            return False


    def get_series_stat(self, series):

        sd = round(np.std(series),2)
        avg = round(np.mean(series),2)
        cv = round((sd/avg)*100,2)

        return (avg, sd, cv)

    def get_bias(self, avg, target):
        try:
            bias = abs(round(float((avg-target)/float(target))*100,2))
        except ZeroDivisionError:
            bias = None
        return bias

    def get_cvt(self,cvw,cva):
        return round(math.sqrt(cva**2 + cvw**2),2)

    def get_allowable_bias(self,cvw,cvb):
        return round(math.sqrt((math.pow(cvw,2) + math.pow(cvb,2)))*0.25,2)

    def get_et(self, target, avg, cv):

        bias = self.get_bias(avg, target)

        return round(bias + (1.65*cv),2)

    def percentage(self, percent, whole):
        return (percent * whole) / 100.0


def main():

    foo = Engine()
    print(foo)
    elements = foo.get_elements()
    print(elements)
    input('end')

if __name__ == "__main__":
    main()
