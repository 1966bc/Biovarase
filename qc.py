#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This is the qc module of Biovarase."""

import numpy as np
import math
import sys
import inspect

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-05-25"
__status__ = "Production"


class QC(object):
    def __init__(self,*args, **kwargs):
        super(QC, self).__init__( *args, **kwargs)

        self.args = args
        self.kwargs = kwargs
        #print("args type: {0} len:{1}".format(type(self.args),len(self.args)))
        
         
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )


    def get_sd(self, values):
        """Standard deviation is a statistic that quantifies how
           close numerical values are in relation to each other.
           The term precision is often used interchangeably with
           standard deviation.
           The repeatability of a test may be
           consistent (low standard deviation, low imprecision)
           or inconsistent (high standard deviation, high
           imprecision)."""

        return round(np.std(values),2)

    def get_cv(self, values):
        """The Coefficient of Variation [CV] is the ratio of the
           standard deviation to the mean and is expressed
           as a percentage."""

        sd = self.get_sd(values)
        mean = self.get_mean(values)
        
        return round((sd/mean)*100,2)

    def get_mean(self, values):
        """To calculate a mean for a specific level of control,
          first, add all the values collected for that control.
          Then divide the sum of these values by the total
          number of values."""
        return round(np.mean(values),2)

    def get_range(self, values):
        """Range is a measure of dispersion which is the difference between 
           the largest and the smallest observed value of a quantitative 
           characteristic in a given sample."""
        
        return round(np.ptp(values),2)

    def get_bias(self, avg, target):
        """Bias is the systematic, signed deviation of the test results
           from the accepted reference value."""

        try:
            bias = abs(round(float((avg-target)/float(target))*100,2))
        except (ZeroDivisionError,ValueError,RuntimeWarning):
            bias = 0
            self.on_log(self,
                       inspect.stack()[0][3],
                       sys.exc_info()[1],
                       sys.exc_info()[0],
                       sys.modules[__name__])
        return bias

    def get_cvt(self,cvw,cva):
        
        return round(math.sqrt(cva**2 + cvw**2),2)

    def get_allowable_bias(self,cvw,cvb):
        """The specification for analytical bias."""
        
        return abs(round(math.sqrt((math.pow(cvw,2) + math.pow(cvb,2)))*0.25,2))

    def get_te(self, target, avg, cv):
        """Compute Totale Error as Te = |Bias| + 1.65 * cv."""
        
        bias = self.get_bias(avg, target)        

        return round(bias + (1.65*cv),2)

    def get_tea(self, cvw, cvb):
        """Compute Totale Error Allowable."""
        
        return round(self.get_allowable_bias(cvw, cvb) + (1.65 * self.get_imp(cvw)),2)
        

    def get_sigma(self, cvw, cvb, target, series):
        """Compute sigma."""
        
        avg = self.get_mean(series)
        tea = self.get_tea(cvw, cvb)
        bias = self.get_bias(avg, target)
        cv = self.get_cv(series)
        sigma = (tea - bias)/cv
        
        return round(sigma,2)


    def get_sce(self, cvw, cvb, target, series):
        """compute delta sistematic critical error."""

        sigma = self.get_sigma(cvw, cvb, target, series)
        sce = round(sigma-1.65,2)
        
        if sce > 3:
            c = "green"
            r = "sce >3"
        elif sce > 2 and sce <= 3:
            c = "yellow"
            r = "2> sce <3"
        elif sce < 2:
            c = "red"
            r = "sce <2"
        else:
            c = None
        return sce,c


    def get_tea_tes_comparision(self, avg, target, cvw, cvb, sd, cva):

        """Confronting total error allowable vs total error instrumental
           
           x = Tea allowable, theoretical
           y = Tes instrumental,  computed"""
        
        try:
            x = round(self.get_allowable_bias(cvw, cvb) + (1.65 * self.get_imp(cvw)),2)
            y = self.get_te(target, avg, cva)
            
            if y < x:
                c = "green"
                r = "<"
            elif y == x:
                c = "yellow"
                r = "="
            elif y > x:
                c = "red"
                r = ">"

            return y,c
        except ZeroDivisionError:
            return None


    def get_imp(self,cvw):
        """The Cotlove/Harris concept defines the maximum allowable imprecision,
           CVA,as the maximum imprecision, that when added to the within-subject
           biological variation, CVw, will maximimally increase the total CV by 12%,
           which is achieved when CVa <= 0.5*CVw"""
        
        return round(cvw*0.5,2)

    def percentage(self, percent, whole):
        return (percent * whole) / 100.0        

        
def main():
    
    foo = QC()
    print(foo)
    series = (4.0, 4.1, 4.0, 4.2, 4.1, 4.1, 4.2)
    mean = foo.get_mean(series)
    print("mean: {0}".format(mean))
    sd = foo.get_sd(series)
    print("sd: {0}".format(sd))
    cv = foo.get_cv(series)
    print("cv: {0}".format(cv))
    input('end')
       
if __name__ == "__main__":
    main()
