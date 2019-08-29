#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This is the westgard module of Biovarase.
    It provides to perform the westgard's rules calculations."""

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-05-22"
__status__ = "Production"


class Westgards:
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.args = args
        self.kwargs = kwargs
        
    def __str__(self):
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__,  [x.__name__ for x in Westgards.__mro__],)

        
    def get_westgard_violation_rule(self, target, sd, series,selected_batch=None, selected_test=None):
        """This function recive target, sd and a value series
           to compute westgard violtetion rule.
 
            @param name: target and sd of the selected batch, series are
                         a list of reversed results of the relative batch
            @return: westgard rule 
            @rtype: string
            """
        
        self.target = target
        self.sd = sd
        self.series = series
        self.selected_batch = selected_batch
        self.selected_test = selected_test
        
        self.get_standard_deviations(target, sd)
    
        if self.get_rule_12S():
            if self.get_rule_13S():
                return "1:3S"
            elif self.get_rule_22S():
                    return "2:2S"
            elif self.get_rule_R4S():
                return "R:4S"
            elif self.get_rule_41S():
                return "4:1S"
            elif self.get_rule_10X():
                return "10:X"
            else:
                return "1:2S"                
        else:
            if self.get_rule_41S():
                return "4:1S"
            else:
                if self.get_rule_10X():
                    return "10:x"
                else:
                    return "Accept"

        
    
    def get_standard_deviations(self,target, sd):

        self.sd1 = target + sd
        self.sd2 = target + (2*sd)
        self.sd3 = target + (3*sd)
        self.sd_1 = target - sd
        self.sd_2 = target - (2*sd)
        self.sd_3 = target - (3*sd)
        self.sd4 = 4*sd

    
    def get_rule_12S(self,):
        """Control data start here.
           1:2s
           Check if the control limits are set as the mean plus/minus 2s
           +/- > 2sd
           If false the value is in control, otherwise we continue the evaluation.
           Refers to the control rule that is commonly used with a Levey-Jennings chart. 
 
            @param name: 
            @return: westgard rule 
            @rtype: string
            """
        #print ("Westgard rule 1:2s tested")
        #print(self.series[-1])

        if self.series[-1] > self.sd2 or  self.series[-1] < self.sd_2:
            return True
        else:
            return False

    def get_rule_13S(self):
        """1:3s
           Check if the control limits are set as the mean plus 3s and the mean minus 3s.
           A run is rejected when a single control measurement exceeds the mean plus 3s
           or the mean minus 3s
           control limit.
           +/- > 3sd"""

        #print ("Westgard rule 1:3s tested")
       
        
        if self.series[-1] > self.sd3  or self.series[-1] < self.sd_3:
            return True
        else:
            return False

    def get_rule_22S(self):
        """2:2s:
           check if 2 consecutive control measurements exceed
           the same mean plus 2s or the same mean minus 2s control limit. """

        #print ("Westgard rule 2:2s tested")

        last_two_values = self.series[-2:]
    

        x = (all(i >= self.sd2 for i in last_two_values))
        y = (all(i <= self.sd_2 for i in last_two_values))

        if x or y:
            return True
        else:
            return False

    def get_rule_R4S(self):
        """R:4s
           Check if 1 control measurement in a group exceeds the mean plus 2s and another
           exceeds the mean minus 2s.
           This rule should only be interpreted within-run, not between-run. """

        #print ("Westgard rule R:4s tested")
        
        last_two_values = self.series[-2:]
        
        a = min(last_two_values)
        b = max(last_two_values)
        value = b - a
        
        if value >= (self.sd4):
            return True
        else:
            return False

    def get_rule_41S(self):
        """4:1s
           Check if 4 consecutive control measurements
           exceed the same mean plus 1s or the same mean minus 1s control limit. """
        
        #print ("Westgard rule 4:1s tested")
        

        last_four_values = self.series[-4:]
        
        x = (all(i > self.sd1 for i in last_four_values))
        y = (all(i < self.sd_1 for i in last_four_values))
        
        if x or y:
            return True
        else:
            return False
                
    def get_rule_10X(self):
        """10:x
           Check when 10 consecutive control measurements fall on one side of the mean."""
        #print ("Westgard rule 10:x tested")
        
        last_ten_values = self.series[-10:]
        
        x = (all(i > self.target for i in last_ten_values))
        y = (all(i < self.target for i in last_ten_values))
        
        if x or y:
            return True
        else:
            return False

        
def main():
    
    foo = Westgards()
    print(foo)

    #(target, sd, series)
    target = 100
    sd = 10
    series = (100,100,100,100,100,100,100,100,100,100,121)
    rule = foo.get_westgard_violation_rule(target, sd, series)
    series = (100,100,110,110,110,110,111,111,111,111,111)
    rule = foo.get_westgard_violation_rule(target, sd, series)
    print(rule)

    input('end')
       
if __name__ == "__main__":
    main()

    
