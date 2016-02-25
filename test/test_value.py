from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import unittest

from measurement_stats import value

class test_value(unittest.TestCase):

    def test_arithmetic(self):
        """ This test is from a problem in Taylor's Error Analysis 3.9 (p. 68)
        """
        l = value.ValueUncertainty(92.95, 0.1)
        T = value.ValueUncertainty(1.936, 0.004)

        g = 4.0 * (math.pi ** 2) * l / (T ** 2)

        self.assertIsInstance(g, value.ValueUncertainty)
        self.assertAlmostEqual(g.value, 979.0)
        self.assertAlmostEqual(g.uncertainty, 4.0)

    def test_roundingIssue(self):
        """ There was a rounding issue that I wanted to check to see was
            correct. This confirms that as strange as it looks, it is correct.
        """

        x1 = value.ValueUncertainty(1.3125, 0.010050373127401788)
        y1 = value.ValueUncertainty(0.2, 0.010050373127401788)
        x2 = value.ValueUncertainty(1.3125, 0.08749999999999997)
        y2 = value.ValueUncertainty(0.0, 0.010050373127401788)

        a = x2 - x1
        a_squared = a ** 2
        b = y2 - y1
        b_squared = b ** 2
        summed = a_squared + b_squared

        result = summed ** 0.5

        print(result)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_value)
    unittest.TextTestRunner(verbosity=2).run(suite)




