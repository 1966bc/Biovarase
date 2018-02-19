#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018
# version:  0.1                                                                
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

    
    def get_rule_12S(self):
        """one value +/- > 2sd"""
        #print "Westgard rule 1:2s tested"
       
        if self.series[0] > self.sd2 or  self.series[0] < self.sd_2:
            return True
        else:
            return False

    def get_rule_13S(self):
        """one value +/- > 3sd"""
        #print "Westgard rule 1:3s tested"
  
        if self.series[0] > self.sd3 or  self.series[0] < self.sd_3:
            return True
        else:
            return False

    def get_rule_22S(self):

        #print "Westgard rule 2:2s tested"

        rule = 2*self.sd
        elements = []
     
        for i in self.series[:2]:
            elements.append(i)

        if (elements[0] > self.sd2 and elements[0] < self.sd3
            and  elements[1] > self.sd2 and elements[1] < self.sd3
            or elements[0] > self.sd_2 and elements[0] < self.sd_3
            and  elements[1] > self.sd_2 and  elements[1] < self.sd_3):
            return True
        
        else:
            return False


    def get_rule_R4S(self):

        #print "Westgard rule R:4s tested"
        elements = []
       
        for i in self.series[:2]:
            elements.append(i)

        a = min(elements)
        b = max(elements)
        value = b - a
        
        if value > (self.sd4):
            return True
        else:
            return False


    def get_rule_41S(self):

        #print "Westgard rule 4:1s tested"
        elements = []
        count = 0   
        
        for i in self.series[:4]:
            elements.append(round(i,2))


        for i in elements:
            if i > (self.sd1):
                count +=1
        
        if count == 4:
            return True
        else:
            count = 0
            
            for i in elements:
                if i < (self.sd_1):
                    count +=1
                          
        if count == 4:
            return True
        else:
            return False
                
                             
    def get_rule_10X(self):

        #print "Westgard rule 10:x tested"
        elements = []
        count = 0
        
        for i in self.series[:10]:
            elements.append(round(i,2))
   
        for i in elements:
            if i > (self.target):
                count +=1
        
        if count == len(elements):
            return True
        else:
            count = 0
            
            for i in elements:
                if i < (self.target):
                    count +=1
                         
        if count == len(elements):
            return True
        else:
            return False

def main():
    
    foo = Westgards()
    print(foo)                
    input('end')
       
if __name__ == "__main__":
    main()

    
