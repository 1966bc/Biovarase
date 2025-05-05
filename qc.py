#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV
# -----------------------------------------------------------------------------
""" This is the qc module of Biovarase."""
import sys
import inspect

import numpy as np
import math

class QC:

    def __str__(self):
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__,
                                             [x.__name__ for x in QC.__mro__],)

    def get_ddof(self):
        """
       Tries to read the ddof value from the 'ddof' file.
        If the file is not found, logs a warning and returns 1 as default.
        """
        try:
            with open('ddof', 'r') as f:
                v = f.readline().strip()
                return int(v)
        except FileNotFoundError:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__],
                        level='warning')
            return 1  # Default value for sample standard deviation
        except ValueError:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__],
                        level='warning')
            return 1 # Default value if file is not valid

    def get_sd(self, values, ddof=None):
        """Standard deviation is a statistic that quantifies how
           close numerical values are in relation to each other.
           The term precision is often used interchangeably with
           standard deviation.
           The repeatability of a test may be
           consistent (low standard deviation, low imprecision)
           or inconsistent (high standard deviation, high
           imprecision)."""
        try:
            a = np.array(values)
            sd = round(np.std(a, ddof=self.get_ddof(), dtype=np.float64), 2)
            return sd

        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None

    def get_cv(self, values, ddof=None):
        """The Coefficient of Variation [CV] is the ratio of the
           standard deviation to the mean and is expressed
           as a percentage."""
        try:
            sd = self.get_sd(values, ddof)
            mean = self.get_mean(values)
            cv = round((sd / mean) * 100, 2)
            return cv
        except ZeroDivisionError as zde:
            self.on_log(inspect.stack()[0][3], zde, type(zde), sys.modules[__name__], level='warning')
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None
        
    def get_mean(self, values):
        """To calculate a mean for a specific level of control,
          first, add all the values collected for that control.
          Then divide the sum of these values by the total
          number of values."""
        try:
            a = np.array(values)
            mean = round(np.mean(a, dtype=np.float64), 2)
            return mean
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None

    def get_range(self, values):
        """Range is a measure of dispersion which is the difference between
           the largest and the smallest observed value of a quantitative
           characteristic in a given sample."""
        try:
            a = np.array(values)
            r = round(np.ptp(a), 2)
            return r
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None
        
    def get_bias(self, avg, target):
        """Bias is the systematic, signed deviation of the test results
           from the accepted reference value."""
        try:
            bias = abs(round(float((avg - target) / float(target)) * 100, 2))
            return bias
        except ZeroDivisionError as zde:
            self.on_log(inspect.stack()[0][3], zde, type(zde), sys.modules[__name__], level='warning')
            return 0  # Or handle as appropriate
        except ValueError as ve:
            self.on_log(inspect.stack()[0][3], ve, type(ve), sys.modules[__name__], level='warning')
            return 0
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return 0

    def get_cvt(self,cvw,cva):
        """The total variation (CVT) is calculated as the square root of the sum of the squares
           of the within-run variation (CVw) and the between-run variation (CVa)."""
        try:
            cvt = round(math.sqrt(cva**2 + cvw**2), 2)
            return cvt
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None

    def get_allowable_bias(self,cvw,cvb):
        """The specification for analytical bias."""
        try:
            allowable_bias = abs(round(math.sqrt((math.pow(cvw, 2) + math.pow(cvb, 2))) * 0.25, 2))        
            return allowable_bias
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None
        
    def get_te(self, target, avg, cv):
        """Compute Totale Error as Te = |Bias| + 1.65 * cv."""
        try:
            bias = self.get_bias(avg, target)
            te = round(bias + (self.get_zscore() * cv), 2)
            return te
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None

    def get_tea(self, cvw, cvb):
        """Compute Totale Error Allowable."""
        try:
            tea = round((self.get_zscore() * self.get_imp(cvw)) +
                        self.get_allowable_bias(cvw, cvb), 2)
            return tea
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None     
        
    def get_sigma(self, cvw, cvb, target, series):
        """Compute sigma."""
        try:
            avg = self.get_mean(series)
            tea = self.get_tea(cvw, cvb)
            bias = self.get_bias(avg, target)
            cv = self.get_cv(series)
            sigma = (tea - bias) / cv
            return round(sigma, 2)
        except ZeroDivisionError as zde:
            self.on_log(inspect.stack()[0][3], zde, type(zde), sys.modules[__name__], level='warning')
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None

    def get_tea_tes_comparision(self, avg, target, cvw, cvb, sd, cva):

        """Confronting total error allowable vs total error instrumental
           
           TEa = allowable, theoretical
           TEobs = instrumental observed,  computed"""
        
        try:
            TEa = round(self.get_allowable_bias(cvw, cvb) +
                        (self.get_zscore() * self.get_imp(cvw)), 2)
            TEobs = self.get_te(target, avg, cva)

            if TEobs < TEa:
                c = "green"
                r = "<"
            elif TEobs == TEa:
                c = "yellow"
                r = "="
            elif TEobs > TEa:
                c = "red"
                r = ">"
            return TEobs, c
        except ZeroDivisionError as zde:
            self.on_log(inspect.stack()[0][3], zde, type(zde), sys.modules[__name__], level='warning')
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None

    def get_imp(self,cvw):
        """The Cotlove/Harris concept defines the maximum allowable imprecision,
           CVA,as the maximum imprecision, that when added to the within-subject
           biological variation, CVw, will maximimally increase the total CV by 12%,
           which is achieved when CVa <= 0.5*CVw"""
        try:
            imp = round(cvw * 0.5, 2)
            return imp
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None

    def percentage(self, percent, whole):
        """Percentage calculation."""
        try:
            result = (percent * whole) / 100.0
            return result
        except TypeError as te:
            self.on_log(inspect.stack()[0][3], te, type(te), sys.modules[__name__], level='warning')
            return None
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error')
            return None

def main():

    foo = QC()
    print(foo)
    #data take from QCWorkbook2008_Jun08.pdf
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
