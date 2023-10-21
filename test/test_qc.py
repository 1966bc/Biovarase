import unittest
import numpy as np

class UBT(unittest.TestCase):

    def setUp(self):
        self.series = (4.0, 4.1, 4.0, 4.2, 4.1, 4.1, 4.2)
  
    # Returns True or False.  
    def test(self):         
        self.assertTrue(True)

    def test_mean(self):
        x = self.get_mean(self.series)
        self.assertEqual(x, 4.1)

    def test_range(self):
        x = self.get_range(self.series)
        self.assertEqual(x, 0.2)        

    def test_sd(self):
        x = self.get_sd(self.series)
        self.assertEqual(x, 0.08)

    def test_cv(self):
        x = self.get_cv(self.series)
        self.assertEqual(x, 1.95)

    def test_bias(self):
        x = self.get_bias(self.series,4)
        self.assertEqual(x, 2.5)           

    def get_mean(self, values):
        """To calculate a mean for a specific level of control,
          first, add all the values collected for that control.
          Then divide the sum of these values by the total
          number of values."""
        a = np.array(values)
        return round(np.mean(a,
                             dtype = np.float64),2)

    def get_sd(self, values, ddof=0):
        """Standard deviation is a statistic that quantifies how
           close numerical values are in relation to each other.
           The term precision is often used interchangeably with
           standard deviation.
           The repeatability of a test may be
           consistent (low standard deviation, low imprecision)
           or inconsistent (high standard deviation, high
           imprecision)."""

        a = np.array(values)
        
        return round(np.std(a,
                            ddof = ddof,
                            dtype = np.float64),2)

    def get_cv(self, values, ddof=0):
        """The Coefficient of Variation [CV] is the ratio of the
           standard deviation to the mean and is expressed
           as a percentage."""
        
        sd = self.get_sd(values, ddof)
        mean = self.get_mean(values)
        return round((sd/mean)*100,2)


    def get_range(self, values):
        """Range is a measure of dispersion which is the difference between 
           the largest and the smallest observed value of a quantitative 
           characteristic in a given sample."""
        a = np.array(values)
        return round(np.ptp(a),2)

    def get_bias(self,  values, target):
        """Bias is the systematic, signed deviation of the test results
           from the accepted reference value."""

        return abs(round(float((self.get_mean(values)-target)/float(target))*100,2))


if __name__ == '__main__': 
    unittest.main() 
