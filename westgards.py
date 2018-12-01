#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn 2018
#-----------------------------------------------------------------------------

class Westgards(object):

    def __init__(self,):
        super(Westgards, self).__init__()

        
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )
        

    def get_violation(self, target, sd, series):

        self.target = target
        self.sd = sd
        self.series = series
        self.get_standard_deviations(sd)

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
            elif self.get_rule_10X():
                return "10:x"
            else:
                return "Accept"
    
    def get_standard_deviations(self,sd):

        self.sd1 = self.target + sd
        self.sd2 = self.target + (2*sd)
        self.sd3 = self.target + (3*sd)
        self.sd_1 = self.target - sd
        self.sd_2 = self.target - (2*sd)
        self.sd_3 = self.target - (3*sd)
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
  
        if self.series[-1] > self.sd3 or  self.series[-1] < self.sd_3:
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
           Check if 1 control measurement in a group exceeds
           the mean plus 2s and another exceeds the mean minus 2s.
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
           Check when 10 consecutive control measurements fall on one
           side of the mean."""
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
    input('end')
       
if __name__ == "__main__":
    main()

    
