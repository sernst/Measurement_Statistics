from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import random

from measurement_stats import angle

class test_angle(unittest.TestCase):

    def test_degrees(self):
        """ doc... """
        for i in range(100):
            value = random.uniform(-2000.0, 5000.0)
            a = angle.Angle(degrees=value)
            self.assertAlmostEqual(a.degrees, value)

        for i in range(100):
            value = random.uniform(-2000.0, 5000.0)
            a = angle.Angle()
            a.degrees = value
            self.assertAlmostEqual(a.degrees, value)

    def test_radians(self):
        """test_radians doc..."""
        for i in range(100):
            value = random.uniform(-2000.0, 5000.0)
            a = angle.Angle(radians=value)
            self.assertAlmostEqual(a.radians, value)

        for i in range(100):
            value = random.uniform(-2000.0, 5000.0)
            a = angle.Angle()
            a.radians = value
            self.assertAlmostEqual(a.radians, value)

    def test_constrainToRevolution(self):
        """test_revolvePositive doc..."""

        for i in range(100):
            value = random.uniform(-2000.0, 5000.0)
            a = angle.Angle(degrees=value)
            a.constrain_to_revolution()
            self.assertLessEqual(a.degrees, 360.0)
            self.assertGreaterEqual(a.degrees, 0.0)

    def test_differenceBetween(self):
        """test_differenceBetween doc..."""

        for i in range(1000):
            value = random.uniform(-2000.0, 5000.0)
            a = angle.Angle(degrees=value)
            a.constrain_to_revolution()

            value = random.uniform(-2000.0, 5000.0)
            b = angle.Angle(degrees=value)
            b.constrain_to_revolution()
            self.assertLessEqual(abs(a.difference_between(b).degrees), 180.0)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_angle)
    unittest.TextTestRunner(verbosity=2).run(suite)

